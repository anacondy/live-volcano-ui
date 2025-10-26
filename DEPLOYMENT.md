# Deployment Guide

## Backend API Deployment

The backend API needs to be deployed to a Python hosting service. Here are recommended options:

### Option 1: Render (Recommended - Free tier available)

1. **Create a Render account** at https://render.com
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api.app:app`
   - Environment Variables:
     - `GEMINI_API_KEY`: Your Gemini API key from https://makersuite.google.com/app/apikey
     - `PORT`: 10000 (or leave blank for Render default)
     - `FLASK_DEBUG`: False

5. **Deploy** and note your service URL (e.g., `https://your-app.onrender.com`)

### Option 2: Heroku

1. **Create a Heroku account** at https://heroku.com
2. **Install Heroku CLI**
3. **Create a Procfile:**
   ```
   web: gunicorn api.app:app
   ```
4. **Deploy:**
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_api_key_here
   git push heroku main
   ```

### Option 3: PythonAnywhere

1. **Create account** at https://www.pythonanywhere.com
2. **Upload code** via Files tab
3. **Create virtual environment** and install dependencies
4. **Configure WSGI** file to point to your Flask app
5. **Set environment variables** in WSGI configuration

### Option 4: Google Cloud Run (Scalable, Pay-per-use)

1. **Create a Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD gunicorn api.app:app --bind 0.0.0.0:$PORT
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy your-service-name \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your_key
   ```

## Frontend Configuration

After deploying the backend:

1. **Update API URL in `static/script.js`:**
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
       ? 'http://localhost:5000'
       : 'https://your-deployed-api-url.com'; // Replace with your actual API URL
   ```

2. **Commit and push** the changes to GitHub
3. **GitHub Pages** will automatically deploy the frontend

## Getting Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and store it securely
5. Add it as an environment variable in your deployment platform

## Security Checklist

- [x] API key stored as environment variable (not in code)
- [x] CORS configured with specific origins
- [x] Rate limiting enabled (20 requests/minute per IP)
- [x] Input validation and sanitization
- [x] Security headers configured
- [x] HTTPS enforced in production
- [x] Content length limits
- [x] Error messages don't leak sensitive info

## Testing the Deployment

1. **Test backend health:**
   ```bash
   curl https://your-api-url.com/api/health
   ```

2. **Test chat endpoint:**
   ```bash
   curl -X POST https://your-api-url.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What are the exam dates?"}'
   ```

3. **Test frontend:** Visit https://anacondy.github.io/live-volcano-ui/

## Local Development

1. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```
   GEMINI_API_KEY=your_key_here
   FLASK_DEBUG=True
   PORT=5000
   ```

3. **Run the backend:**
   ```bash
   python api/app.py
   ```

4. **Serve the frontend:**
   ```bash
   python -m http.server 8080
   ```

5. **Open browser:** http://localhost:8080

## Troubleshooting

### CORS Errors
- Ensure your API URL is correctly configured in `script.js`
- Check that CORS origins include your GitHub Pages domain

### API Not Responding
- Verify the API is running: check health endpoint
- Check environment variables are set correctly
- Review server logs for errors

### Gemini API Errors
- Verify API key is valid
- Check API quota/billing status
- Review API request logs

### Slow Response Times
- Cache is configured for 5 minutes - first request may be slow
- Consider using a caching service (Redis) for better performance
- Check network latency between services

## Monitoring

- Enable logging in your deployment platform
- Set up uptime monitoring (e.g., UptimeRobot, Pingdom)
- Monitor API usage and quota
- Track error rates and response times
