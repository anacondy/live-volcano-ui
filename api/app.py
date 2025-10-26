"""
Backend API for Gemini 2.5 Pro integration with Subodh College website
Provides secure, intelligent responses to student queries
"""

import os
import re
import time
import logging
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS with security
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://anacondy.github.io",
            "http://localhost:*",
            "http://127.0.0.1:*"
        ],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Rate limiting for security
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"],
    storage_uri="memory://"
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# College website constants
COLLEGE_URL = "https://www.subodhpgcollege.com/"
CACHE_DURATION = 300  # 5 minutes cache for scraped data

# Cache for scraped content
content_cache = {
    'data': None,
    'timestamp': 0
}


class CollegeWebsiteScraper:
    """Scraper for Subodh College website"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """Scrape a single page"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Error scraping {url}: {e}")
            return None
    
    def extract_text_from_html(self, html: str) -> str:
        """Extract clean text from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def scrape_relevant_sections(self) -> Dict[str, str]:
        """Scrape relevant sections of the college website"""
        sections = {}
        
        # Main pages to scrape
        pages_to_scrape = [
            ('home', ''),
            ('news', 'news/'),
            ('notifications', 'notifications/'),
            ('exams', 'examinations/'),
            ('syllabus', 'syllabus/'),
        ]
        
        for section_name, path in pages_to_scrape:
            url = urljoin(self.base_url, path)
            html = self.scrape_page(url)
            if html:
                text = self.extract_text_from_html(html)
                sections[section_name] = text[:5000]  # Limit text length
        
        return sections


def get_college_context() -> Dict[str, str]:
    """Get college website context with caching"""
    current_time = time.time()
    
    # Return cached data if still valid
    if (content_cache['data'] and 
        current_time - content_cache['timestamp'] < CACHE_DURATION):
        return content_cache['data']
    
    # Scrape fresh data
    scraper = CollegeWebsiteScraper(COLLEGE_URL)
    data = scraper.scrape_relevant_sections()
    
    # Update cache
    content_cache['data'] = data
    content_cache['timestamp'] = current_time
    
    return data


def normalize_query(query: str) -> str:
    """Normalize user query for better understanding"""
    query = query.lower()
    
    # Convert Roman numerals to ordinal numbers
    roman_to_ordinal = {
        'i': '1st', 'ii': '2nd', 'iii': '3rd', 'iv': '4th',
        'v': '5th', 'vi': '6th', 'vii': '7th', 'viii': '8th'
    }
    
    for roman, ordinal in roman_to_ordinal.items():
        # Match "III sem" or "iii semester"
        query = re.sub(
            rf'\b{roman}\s+(sem|semester)\b',
            f'{ordinal} semester',
            query,
            flags=re.IGNORECASE
        )
    
    return query


def generate_prompt(user_query: str, college_context: Dict[str, str]) -> str:
    """Generate prompt for Gemini with context"""
    normalized_query = normalize_query(user_query)
    
    # Build context from scraped data
    context_text = ""
    for section, content in college_context.items():
        if content:
            context_text += f"\n\n=== {section.upper()} SECTION ===\n{content}"
    
    prompt = f"""You are a helpful assistant for Subodh PG College students. You have access to the college website information.

College Website: {COLLEGE_URL}

Available Information from College Website:
{context_text}

Student Question: {normalized_query}

Instructions:
1. If the question is about Subodh PG College (exams, dates, news, notifications, forms, holidays, etc.), search the provided context carefully
2. Give SHORT, PRECISE, and TO-THE-POINT answers
3. Format dates clearly (e.g., "29 Oct, 2025 (1st shift)")
4. If information is not found in the context, politely say you don't have that specific information and suggest checking the college website
5. Be intelligent - understand context like "III sem" means "3rd semester"
6. Keep responses under 2-3 sentences unless more detail is absolutely necessary
7. By default, assume questions are about Subodh PG College unless stated otherwise

Provide a concise, helpful answer:"""
    
    return prompt


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model': 'gemini-2.0-flash-exp'})


@app.route('/api/chat', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    """Main chat endpoint"""
    try:
        # Get user message
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Limit message length for security
        if len(user_message) > 500:
            return jsonify({'error': 'Message too long (max 500 characters)'}), 400
        
        # Get college context
        college_context = get_college_context()
        
        # Generate prompt
        prompt = generate_prompt(user_message, college_context)
        
        # Generate response with Gemini
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=200,  # Keep responses short
                top_p=0.9,
                top_k=40
            ),
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        )
        
        # Extract response text
        bot_response = response.text.strip()
        
        return jsonify({
            'response': bot_response,
            'timestamp': time.time()
        })
    
    except Exception as e:
        # Log error internally but don't expose details to user
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        
        return jsonify({
            'error': 'An error occurred processing your request. Please try again later.'
        }), 500


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    # Development server - do not use in production
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
