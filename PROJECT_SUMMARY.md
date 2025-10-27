# Project Summary

## Overview
Live Volcano UI is an interactive web application with a beautiful particle-animated background, now enhanced with Google Gemini 2.5 Pro AI integration to provide intelligent responses about Subodh PG College.

## Architecture

### Frontend (Static - GitHub Pages)
- **Technology**: HTML5, CSS3, Vanilla JavaScript
- **Hosting**: GitHub Pages (https://anacondy.github.io/live-volcano-ui/)
- **Features**:
  - Particle animation with Perlin noise (500 particles)
  - Mouse interaction effects
  - Smooth text animations
  - Responsive design (mobile + desktop)
  - API integration via fetch

### Backend (Python - Deployed separately)
- **Technology**: Flask, Gunicorn
- **Hosting**: Render/Heroku/PythonAnywhere/Cloud Run
- **Features**:
  - Gemini 2.5 Pro API integration
  - Web scraping (BeautifulSoup)
  - Caching (5-minute TTL)
  - Rate limiting (Flask-Limiter)
  - CORS protection
  - Security headers

## Key Features

### AI Capabilities
1. **Context-Aware Understanding**: Converts "III sem" to "3rd semester"
2. **Website Search**: Scrapes Subodh College website for current information
3. **Short Responses**: Limited to 200 tokens for concise answers
4. **Smart Prompting**: Includes scraped context in Gemini prompts
5. **Caching**: 5-minute cache reduces load and improves response time

### Security Features
1. **API Key Protection**: Environment variables only
2. **Rate Limiting**: 20 req/min per IP, 100 req/hour per IP
3. **CORS**: Whitelist of allowed origins
4. **Input Validation**: Max 500 chars, non-empty checks
5. **Security Headers**: XSS, clickjacking, MIME sniffing protection
6. **Content Safety**: Gemini safety filters enabled
7. **Error Handling**: No stack trace exposure
8. **Dependencies**: All vulnerabilities fixed (gunicorn 22.0.0)
9. **Logging**: Proper logging framework (no sensitive data in logs)

### Performance Optimizations
1. **Text Rendering**: requestAnimationFrame for smooth 60 FPS
2. **API Caching**: 5-minute cache for scraped content
3. **Lazy Loading**: Efficient resource loading
4. **Minimal Dependencies**: Small bundle size

## File Structure
```
live-volcano-ui/
├── api/
│   └── app.py              # Flask backend server
├── static/
│   ├── config.js           # API URL configuration
│   ├── script.js           # Frontend JavaScript
│   └── style.css           # Styles and animations
├── index.html              # Main HTML file
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment
├── runtime.txt            # Python version
├── app.json               # Heroku/Render config
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
├── README.md              # Main documentation
├── QUICKSTART.md          # Quick start guide
├── DEPLOYMENT.md          # Deployment guide
├── SECURITY.md            # Security documentation
├── TESTING.md             # Testing guide
└── LICENSE                # MIT License
```

## Dependencies

### Backend (Python)
- Flask 3.0.0 - Web framework
- flask-cors 4.0.0 - CORS handling
- Flask-Limiter 3.5.0 - Rate limiting
- google-generativeai 0.3.2 - Gemini API
- requests 2.31.0 - HTTP client
- beautifulsoup4 4.12.2 - Web scraping
- python-dotenv 1.0.0 - Environment variables
- gunicorn 22.0.0 - WSGI server (production)
- lxml 5.1.0 - HTML parser

### Frontend (JavaScript)
- No external dependencies
- Pure vanilla JavaScript
- Uses native Fetch API
- Google Fonts (Alex Brush)

## API Endpoints

### GET /api/health
Health check endpoint
**Response:** `{"status": "healthy", "model": "gemini-2.0-flash-exp"}`

### POST /api/chat
Main chat endpoint
**Request:** `{"message": "user question"}`
**Response:** `{"response": "AI response", "timestamp": 1234567890.123}`
**Rate Limit:** 20/minute per IP

## Configuration

### Environment Variables
- `GEMINI_API_KEY` (required) - Gemini API key
- `PORT` (optional) - Server port (default: 5000)
- `FLASK_DEBUG` (optional) - Debug mode (default: False)

### Frontend Config
Edit `static/config.js`:
- `LOCAL_API_URL` - Local development API
- `PRODUCTION_API_URL` - Production API URL

## Deployment

### Backend Deployment Options
1. **Render** (Recommended) - Free tier, automatic deployments
2. **Heroku** - Easy deployment, free tier available
3. **PythonAnywhere** - Python-specific hosting
4. **Google Cloud Run** - Serverless, pay-per-use

### Frontend Deployment
- Automatically deployed via GitHub Pages
- Any push to main branch updates the live site
- URL: https://anacondy.github.io/live-volcano-ui/

## Testing

### Manual Testing
- Frontend visual testing
- Backend API testing with curl
- Integration testing
- Cross-browser testing

### Security Testing
- Rate limiting verification
- Input validation testing
- CORS testing
- Security header verification
- CodeQL scanning (all checks passed)

### Performance Testing
- Text animation smoothness (60 FPS)
- API response time (<3s first, <1s cached)
- Load testing with Apache Bench

## Security Status
✅ All CodeQL security checks passed
✅ No known vulnerabilities in dependencies
✅ Input validation and sanitization
✅ Rate limiting active
✅ Security headers configured
✅ API key properly protected
✅ No sensitive data exposure
✅ Proper error handling

## Known Limitations
1. First API request is slower (web scraping)
2. College website structure changes may break scraping
3. No authentication on chat endpoint (rate limiting only)
4. Public API URL is visible in frontend code
5. Cache is in-memory (resets on server restart)

## Future Enhancements
1. Add authentication for chat API
2. Use Redis for distributed caching
3. Add database for analytics and logging
4. Implement WebSocket for real-time updates
5. Add user sessions and history
6. Implement A/B testing for responses
7. Add more college websites
8. Improve error recovery and fallbacks
9. Add unit and integration tests
10. Implement CI/CD pipeline

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Monitor API usage and costs
- Review security advisories
- Check website scraping still works
- Monitor error logs
- Update documentation

### Monitoring
- Server uptime
- API response times
- Error rates
- Rate limit hits
- API quota usage

## Support
- GitHub Issues: https://github.com/anacondy/live-volcano-ui/issues
- Documentation: See README.md and related guides
- Community: GitHub Discussions (if enabled)

## License
MIT License - See LICENSE file

## Credits
- Original UI design: anacondy
- Gemini AI: Google
- Particle animation: Perlin noise algorithm
- Font: Google Fonts (Alex Brush)

## Version History
- v2.0.0 - Gemini AI integration with secure backend
- v1.0.0 - Initial release with particle animation UI

## Contact
Repository: https://github.com/anacondy/live-volcano-ui
Author: anacondy
