"""
Backend API for Gemini 2.5 Pro integration with Subodh College website
Provides secure, intelligent responses to student queries
"""

import os
import re
import time
import logging
import io
import threading
from typing import Dict, Optional, List
from urllib.parse import urljoin, urlparse

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import PyPDF2
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

# Resolve project paths for serving frontend files from the backend.
API_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(API_DIR)
FRONTEND_STATIC_DIR = os.path.join(API_DIR, 'static')

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

# Prefer stable production model names and gracefully fall back if one is unavailable.
DEFAULT_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash').strip()


def model_name_variants(name: str) -> List[str]:
    """Support both `models/...` and plain model names for compatibility."""
    if name.startswith('models/'):
        return [name, name.replace('models/', '', 1)]
    return [name, f'models/{name}']


FALLBACK_MODELS = list(dict.fromkeys(
    model_name_variants(DEFAULT_MODEL) +
    model_name_variants('gemini-2.5-flash') +
    model_name_variants('gemini-2.5-flash-lite') +
    model_name_variants('gemini-2.0-flash') +
    model_name_variants('gemini-1.5-flash') +
    model_name_variants('gemini-1.5-flash-8b')
))

runtime_state = {
    'last_model_error': None,
    'last_success_at': None
}


def get_candidate_models() -> List[str]:
    """Build a robust candidate model list from configured and available models."""
    candidates = list(dict.fromkeys(FALLBACK_MODELS))
    try:
        for model in genai.list_models():
            model_name = getattr(model, 'name', '')
            methods = getattr(model, 'supported_generation_methods', []) or []
            if model_name and 'generateContent' in methods:
                candidates.append(model_name)
    except Exception as e:
        logger.warning(f"Could not list Gemini models; using fallback names only: {e}")

    # De-duplicate while preserving order.
    return list(dict.fromkeys(candidates))

# College website constants
COLLEGE_URL = "https://www.subodhpgcollege.com/"
CACHE_DURATION = 300  # 5 minutes cache for scraped data

# Cache for scraped content
content_cache = {
    'data': None,
    'timestamp': 0,
    'is_fetching': False
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

    def read_pdf(self, pdf_url: str) -> str:
        """Fetch and extract text from a PDF securely and quickly"""
        try:
            res = self.session.get(pdf_url, timeout=10)
            res.raise_for_status()
            reader = PyPDF2.PdfReader(io.BytesIO(res.content))
            text_pages = []
            for i, page in enumerate(reader.pages):
                # Ensure we only process a limited number of pages to stay snappy
                if i >= 5: break 
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text.strip())
            return " ".join(text_pages)
        except Exception as e:
            logger.warning(f"Failed to read PDF at {pdf_url}: {e}")
            return ""
            
    def _extract_lists_and_pdfs(self, html: str, page_url: str) -> str:
        """Specifically look for lists, tables, notice links and parse up to 3 recent PDFs"""
        soup = BeautifulSoup(html, 'html.parser')
        extracted_info = []
        
        # Look for standard notice wrappers and rows
        rows = soup.find_all(['tr', 'li', 'div'], class_=re.compile(r'notice|exam|row|item', re.I))
        if not rows:
            rows = soup.find_all('a', href=re.compile(r'\.pdf|notice|exam', re.I))
            
        count = 0
        for element in rows:
            if count >= 10: break # Keep context tight
            text = element.get_text(separator=' ', strip=True)
            if not text: continue
            
            link = element.find('a', href=True) if element.name != 'a' else element
            pdf_content = ""
            
            if link and link.get('href'):
                href = link['href']
                full_link = urljoin(page_url, href)
                if href.lower().endswith('.pdf') and count < 3: # Only read top 3 PDFs to stay fast
                    pdf_text = self.read_pdf(full_link)
                    if pdf_text:
                        pdf_content = f" [PDF CONTENT: {pdf_text[:1000]}...]"
            
            extracted_info.append(f"- {text} {pdf_content}")
            count += 1
            
        return "\n".join(extracted_info)
        
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
        """Scrape relevant sections and pre-cache them"""
        sections = {}
        
        # Target specific URls requested
        pages_to_scrape = [
            ('notice_board', 'notice_board'),
            ('examination_news', 'examination_news'),
            ('home', ''),
        ]
        
        for section_name, path in pages_to_scrape:
            # Subodh site urls uses absolute routing in user requests
            url = urljoin(self.base_url, path)
            html = self.scrape_page(url)
            if html:
                # Use enriched PDF extractor for notice and exam boards
                if 'notice' in section_name or 'exam' in section_name:
                    enriched = self._extract_lists_and_pdfs(html, url)
                    sections[section_name] = enriched[:8000] # Fit in standard context models
                else:
                    text = self.extract_text_from_html(html)
                    sections[section_name] = text[:4000]
        
        return sections


def update_cache_background():
    """Background task to fetch all college data without blocking the user"""
    if content_cache['is_fetching']:
        return
    try:
        content_cache['is_fetching'] = True
        logger.info("Starting background scrape of Subodh College data...")
        scraper = CollegeWebsiteScraper(COLLEGE_URL)
        data = scraper.scrape_relevant_sections()
        
        content_cache['data'] = data
        content_cache['timestamp'] = time.time()
        logger.info("Background scrape complete. Cache updated.")
    except Exception as e:
        logger.error(f"Background scrape failed: {e}")
    finally:
        content_cache['is_fetching'] = False

def get_college_context() -> Dict[str, str]:
    """Get college website context with background caching"""
    current_time = time.time()
    
    # Needs refresh if cache is None or older than CACHE_DURATION
    needs_refresh = (not content_cache['data'] or 
                     current_time - content_cache['timestamp'] > CACHE_DURATION)
                     
    if needs_refresh and not content_cache['is_fetching']:
        # Fire background thread
        thread = threading.Thread(target=update_cache_background)
        thread.daemon = True
        thread.start()
        
        # If cache is entirely empty, wait very briefly or return empty to keep it snappy.
        # But for AI accuracy, block a little bit on the first ever request.
        if not content_cache['data']:
            thread.join(timeout=8.0) # Wait up to 8s for the first run
            
    return content_cache['data'] or {}


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
    
    prompt = f"""You are a smart, fast assistant for SS Jain Subodh PG Autonomous College students. 
You extract info directly from the parsed college website data and PDF contents provided in the context below.

Context from website (Notice boards, Announcements, Extracted PDFs):
{context_text}

Student Question: {normalized_query}

CRITICAL Instructions:
1. You MUST answer specifically based on the context above. Extract exact dates if asked.
2. Tone must be direct and concise. No intro lines, no filler, no repeated explanation.
3. Default output limit: maximum 2 short sentences OR maximum 3 bullet points.
4. Only use a Markdown table when the user explicitly asks for table format or multiple date rows are necessary.
5. If user asks in Hindi, answer in Hindi (or clean translation) concisely.
6. Understand terms like "III sem" = "3rd semester", "I sem" = "1st Semester".
7. Format dates cleanly (e.g., "**29 Oct, 2025 (1st shift)**").

Provide your helpful and accurate answer now:"""
    
    return prompt


def compact_response_text(text: str) -> str:
    """Keep responses short and readable for UI display."""
    cleaned = re.sub(r'\s+', ' ', (text or '').strip())
    if not cleaned:
        return cleaned

    # Preserve table/list formatting when model intentionally returns structured data.
    if '|' in cleaned or cleaned.lstrip().startswith('-'):
        return cleaned[:700]

    sentences = re.split(r'(?<=[.!?])\s+', cleaned)
    concise = ' '.join(sentences[:2]).strip()
    return concise[:320]


@app.route('/', methods=['GET'])
def serve_index():
    """Serve the frontend entrypoint."""
    return send_from_directory(PROJECT_ROOT, 'index.html')


@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename: str):
    """Serve frontend static assets."""
    return send_from_directory(FRONTEND_STATIC_DIR, filename)


@app.route('/api/static/<path:filename>', methods=['GET'])
def serve_api_static(filename: str):
    """Serve frontend static assets via API namespace for Vercel reliability."""
    return send_from_directory(FRONTEND_STATIC_DIR, filename)


@app.route('/<path:path>', methods=['GET'])
def serve_spa_fallback(path: str):
    """Route all non-API paths to the SPA entrypoint."""
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory(PROJECT_ROOT, 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': DEFAULT_MODEL,
        'keyConfigured': bool(GEMINI_API_KEY),
        'degraded': runtime_state['last_model_error'] is not None,
        'lastModelError': runtime_state['last_model_error'],
        'lastSuccessAt': runtime_state['last_success_at']
    })


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
        
        response = None
        model_error = None

        # Try preferred model first, then robust fallbacks including discovered models.
        for model_name in get_candidate_models():
            try:
                active_model = genai.GenerativeModel(model_name)
                response = active_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.2,
                        max_output_tokens=180,
                        top_p=0.8,
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
                if response and getattr(response, 'text', None):
                    break
            except Exception as e:
                model_error = e
                logger.warning(f"Model {model_name} failed, trying next fallback: {e}")

        if not response or not getattr(response, 'text', None):
            runtime_state['last_model_error'] = type(model_error).__name__ if model_error else 'UnknownModelError'
            logger.error(f"All configured Gemini models failed: {model_error}")
            return jsonify({
                'response': 'I am temporarily unable to generate a live answer right now. Please try again in a moment.',
                'timestamp': time.time(),
                'degraded': True
            })

        # Extract response text
        bot_response = compact_response_text(response.text)
        runtime_state['last_model_error'] = None
        runtime_state['last_success_at'] = time.time()
        
        return jsonify({
            'response': bot_response,
            'timestamp': time.time()
        })
    
    except Exception as e:
        # Log error internally but don't expose details to user
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)

        return jsonify({
            'response': 'I am temporarily unavailable due to a server issue. Please try again shortly.',
            'timestamp': time.time(),
            'degraded': True
        })


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
