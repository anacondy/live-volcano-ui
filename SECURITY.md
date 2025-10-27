# Security Documentation

## Security Features Implemented

### 1. API Key Protection
- **Environment Variables**: Gemini API key stored in `.env` file, never in source code
- **Git Ignore**: `.env` file excluded from version control via `.gitignore`
- **Documentation**: `.env.example` provided for reference without exposing secrets

### 2. Rate Limiting
- **Flask-Limiter**: Implements rate limiting to prevent abuse
- **Limits**:
  - 100 requests per hour per IP
  - 20 requests per minute per IP
- **Protection**: Prevents DDoS attacks and API abuse

### 3. CORS (Cross-Origin Resource Sharing)
- **Restricted Origins**: Only allows requests from:
  - `https://anacondy.github.io` (GitHub Pages)
  - `localhost` (development)
  - `127.0.0.1` (development)
- **Methods**: Only POST requests allowed for chat endpoint
- **Headers**: Restricted to Content-Type header

### 4. Input Validation
- **Length Limits**: 
  - User messages limited to 500 characters
  - Prevents memory exhaustion attacks
- **Empty Check**: Rejects empty messages
- **Sanitization**: Input trimmed and validated before processing

### 5. Security Headers
All API responses include security headers:
- **X-Content-Type-Options**: nosniff (prevents MIME sniffing)
- **X-Frame-Options**: DENY (prevents clickjacking)
- **X-XSS-Protection**: 1; mode=block (XSS protection)
- **Strict-Transport-Security**: HTTPS enforcement
- **Content-Security-Policy**: Restricts resource loading

### 6. Content Safety
- **Gemini Safety Settings**: Configured to block:
  - Harassment
  - Hate speech
  - Sexually explicit content
  - Dangerous content
- **Threshold**: BLOCK_MEDIUM_AND_ABOVE

### 7. Output Restrictions
- **Token Limits**: Gemini responses limited to 200 tokens
- **Prevents**: Large response attacks and excessive API usage
- **User Experience**: Ensures concise, relevant answers

### 8. Error Handling
- **Generic Errors**: Production mode doesn't expose internal details
- **Logging**: Errors logged server-side, not sent to client
- **Graceful Degradation**: Friendly error messages for users

### 9. Session Management
- **Stateless**: No session data stored server-side
- **No Cookies**: No authentication cookies to steal
- **Simple**: Reduces attack surface

### 10. Web Scraping Safety
- **Timeout**: 10-second timeout prevents hanging requests
- **User Agent**: Identifies as a bot for transparency
- **Caching**: Reduces load on target website
- **Respectful**: 5-minute cache prevents excessive requests

### 11. Dependencies Security
All dependencies are pinned to specific versions:
- Regular security updates recommended
- Known vulnerabilities tracked via GitHub Dependabot
- Minimal dependency footprint

## Secure Development Practices

### Code Review
- No hardcoded secrets
- No SQL injection vectors (no database)
- No command injection vectors
- No path traversal vulnerabilities

### Transport Security
- **HTTPS Only**: Enforced in production via security headers
- **TLS**: Minimum version 1.2 recommended
- **Certificate**: Valid SSL certificate required for production

### Deployment Security
- **Environment Isolation**: Separate dev/staging/production environments
- **Secret Management**: Use platform-specific secret management (Render, Heroku, etc.)
- **Monitoring**: Enable logging and monitoring in production
- **Updates**: Keep Python and dependencies updated

## Vulnerability Response Plan

### If a security issue is found:
1. **Report**: Email repository owner or create private security advisory
2. **Assessment**: Evaluate severity and impact
3. **Patch**: Develop and test fix
4. **Deploy**: Update production immediately for critical issues
5. **Notify**: Inform users if their data might be affected
6. **Document**: Add to security changelog

## Security Checklist for Deployment

- [ ] Gemini API key stored as environment variable
- [ ] HTTPS enabled and enforced
- [ ] CORS configured with specific origins
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Error messages don't expose internal details
- [ ] Logging enabled for security events
- [ ] Monitoring and alerting configured
- [ ] Dependencies updated to latest secure versions
- [ ] API endpoint URLs updated in frontend
- [ ] Test security headers with https://securityheaders.com
- [ ] Test SSL configuration with https://www.ssllabs.com

## Known Limitations

### Public API
- The chat API is public (no authentication)
- Rate limiting is the primary defense
- Consider adding API key authentication for production

### Web Scraping
- Dependent on college website structure
- May break if website changes
- No authentication for college website access

### Client-Side Security
- Frontend code is public (JavaScript)
- API URL visible to users
- Cannot hide backend endpoint completely

## Recommendations for Production

1. **Add Authentication**: Implement API key or OAuth for chat endpoint
2. **Database**: Add database for logging and analytics
3. **Monitoring**: Use services like Sentry for error tracking
4. **CDN**: Use CDN for DDoS protection (Cloudflare)
5. **Backup**: Implement regular backup of logs and data
6. **Audit**: Regular security audits and penetration testing
7. **WAF**: Consider Web Application Firewall in production

## Security Testing

### Manual Tests
```bash
# Test rate limiting
for i in {1..25}; do curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'; done

# Test input validation
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'

# Test long input
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "'$(python -c 'print("a"*600)')'"}'

# Test CORS
curl -X POST http://localhost:5000/api/chat \
  -H "Origin: https://malicious-site.com" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' -v
```

### Automated Testing
Consider adding:
- OWASP ZAP for vulnerability scanning
- Bandit for Python security linting
- Safety for dependency vulnerability checking

## Contact

For security concerns, please contact the repository maintainer through GitHub.
