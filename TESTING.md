# Testing Guide

## Quick Start Testing

### 1. Test Frontend (Static Site)

The frontend can work independently with a fallback message when the backend is not available.

```bash
# Serve the frontend
python -m http.server 8080

# Open browser
# Navigate to: http://localhost:8080
```

**Expected behavior:**
- Beautiful particle animation background
- Input field with glow effect on focus
- Typing and pressing Enter shows "Thinking..." then an error message about backend connection

### 2. Test Backend API

#### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

#### Start the backend
```bash
python api/app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
```

#### Test health endpoint
```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{"model": "gemini-2.0-flash-exp", "status": "healthy"}
```

#### Test chat endpoint (without Gemini - will fail gracefully)
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

**Expected response (if GEMINI_API_KEY is not set):**
```json
{"error": "An error occurred processing your request"}
```

**Expected response (if GEMINI_API_KEY is set):**
```json
{"response": "...", "timestamp": 1234567890.123}
```

### 3. Test Full Integration

#### Setup
1. Start backend (Terminal 1):
```bash
python api/app.py
```

2. Start frontend (Terminal 2):
```bash
python -m http.server 8080
```

3. Open browser: http://localhost:8080

#### Test Cases

##### Test Case 1: Basic Question
**Input:** "Hello"
**Expected:** Friendly greeting response

##### Test Case 2: College-Specific Query
**Input:** "When is the III sem exam?"
**Expected:** Response with exam information or message indicating data not available

##### Test Case 3: Context Understanding
**Input:** "III sem elementary computer application exam date"
**Expected:** Intelligent response understanding "III" means "3rd semester"

##### Test Case 4: Form Status
**Input:** "Are exam forms live?"
**Expected:** Information about form availability or instruction to check website

##### Test Case 5: Empty Input
**Input:** "" (empty)
**Expected:** No request sent, input field remains active

##### Test Case 6: Long Input (500+ chars)
**Input:** Very long text
**Expected:** Error message about message length

## Manual Testing Checklist

### Frontend
- [ ] Page loads without errors
- [ ] Particle animation renders smoothly
- [ ] Input field glows on focus
- [ ] Mouse interaction affects particles
- [ ] Text appears smoothly without lag
- [ ] Message stays visible for at least 4 seconds
- [ ] Message clears when typing starts
- [ ] Responsive on mobile
- [ ] Works in different browsers (Chrome, Firefox, Safari)

### Backend
- [ ] Health endpoint responds
- [ ] Chat endpoint accepts POST requests
- [ ] CORS headers present
- [ ] Rate limiting works (test with multiple requests)
- [ ] Security headers present
- [ ] Invalid input rejected (empty, too long)
- [ ] Errors don't expose internal details
- [ ] API key required for startup

### Integration
- [ ] Frontend calls backend API
- [ ] Loading state shows "Thinking..."
- [ ] Response displays with animation
- [ ] Error handling works gracefully
- [ ] Multiple consecutive messages work
- [ ] College website data is fetched and cached

## Performance Testing

### Text Rendering Performance
1. Open browser DevTools
2. Go to Performance tab
3. Type a message and press Enter
4. Check that animation is smooth (60 FPS)
5. No lag or stuttering should occur

### API Response Time
```bash
# Test response time
time curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

**Expected:** < 3 seconds (first request may be slower due to scraping)
**Expected:** < 1 second (subsequent requests use cache)

### Load Testing
```bash
# Install apache bench
sudo apt-get install apache2-utils

# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 -p test_payload.json -T application/json \
  http://localhost:5000/api/chat
```

## Security Testing

### Rate Limiting
```bash
# Send 25 requests rapidly
for i in {1..25}; do 
  curl -X POST http://localhost:5000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "test"}' -s -o /dev/null -w "%{http_code}\n"
done
```

**Expected:** First ~20 return 200, then 429 (Too Many Requests)

### Input Validation
```bash
# Test empty input
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}' -w "\n%{http_code}\n"

# Test long input
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$(python3 -c 'print("a"*600)')\"}" -w "\n%{http_code}\n"

# Test missing message field
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{}' -w "\n%{http_code}\n"
```

**Expected:** All should return 400 with error messages

### Security Headers
```bash
curl -I http://localhost:5000/api/health
```

**Expected headers:**
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000

### CORS Testing
```bash
# Test from unauthorized origin
curl -X POST http://localhost:5000/api/chat \
  -H "Origin: https://malicious-site.com" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' \
  -v 2>&1 | grep -i "access-control"
```

**Expected:** Access-Control-Allow-Origin should NOT include malicious-site.com

## Automated Testing (Future Enhancement)

### Python Unit Tests
Create `tests/test_app.py`:
```python
import pytest
from api.app import app, normalize_query

def test_normalize_query():
    assert "3rd semester" in normalize_query("III sem exam")
    assert "1st semester" in normalize_query("i semester")

def test_health_endpoint():
    client = app.test_client()
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

# Add more tests...
```

Run with:
```bash
pip install pytest
pytest tests/
```

### JavaScript Tests (Future)
- Use Jest for unit testing
- Test API calls with mocked responses
- Test animation functions
- Test input validation

## Browser Testing Matrix

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | ✓ Primary |
| Firefox | Latest | ✓ Supported |
| Safari | Latest | ✓ Supported |
| Edge | Latest | ✓ Supported |
| Mobile Safari | iOS 14+ | ✓ Supported |
| Chrome Mobile | Latest | ✓ Supported |

## Known Issues and Limitations

1. **First Request Slow**: First API request is slower due to web scraping
2. **Website Changes**: If college website structure changes, scraping may break
3. **No Offline Mode**: Requires backend API to be running
4. **Rate Limits**: Aggressive rate limiting may affect legitimate users
5. **Mobile Keyboard**: On mobile, keyboard may cover input on some devices

## Debugging Tips

### Frontend Issues
- Check browser console for errors (F12)
- Verify config.js has correct API URL
- Check Network tab for failed API calls
- Disable browser extensions that may block requests

### Backend Issues
- Check Python terminal for error messages
- Verify .env file exists and has GEMINI_API_KEY
- Check that port 5000 is not in use
- Verify all dependencies installed (`pip list`)
- Test with curl to isolate frontend/backend issues

### API Issues
- Verify Gemini API key is valid
- Check API quota/billing status
- Test with a simple direct API call
- Check network connectivity

## Reporting Bugs

When reporting issues, include:
1. Browser/OS version
2. Error messages (screenshot)
3. Network tab screenshot (if API issue)
4. Steps to reproduce
5. Expected vs actual behavior
