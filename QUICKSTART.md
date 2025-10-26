# Quick Start Guide

Get your Live Volcano UI with Gemini AI up and running in minutes!

## For Users (GitHub Pages)

Just visit the live site:
👉 **https://anacondy.github.io/live-volcano-ui/**

**Note:** The AI features require a backend API to be deployed. Without the backend, the UI will show connection errors. See the deployment section below.

## For Developers

### Prerequisites
- Python 3.11+
- Git
- Gemini API Key (get from https://makersuite.google.com/app/apikey)

### Local Development Setup (5 minutes)

1. **Clone the repository:**
```bash
git clone https://github.com/anacondy/live-volcano-ui.git
cd live-volcano-ui
```

2. **Set up Python environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. **Run backend (Terminal 1):**
```bash
python api/app.py
```

5. **Run frontend (Terminal 2):**
```bash
python -m http.server 8080
```

6. **Open browser:**
```
http://localhost:8080
```

7. **Try it out:**
Type a question like "When is the III sem exam?" and press Enter!

## Production Deployment (10 minutes)

### Deploy Backend to Render (Free)

1. **Create Render account:** https://render.com
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api.app:app`
   - Add Environment Variable: `GEMINI_API_KEY` = your_key
5. **Deploy!**
6. **Copy your service URL** (e.g., `https://your-app.onrender.com`)

### Update Frontend Configuration

1. **Edit `static/config.js`:**
```javascript
PRODUCTION_API_URL: 'https://your-app.onrender.com'  // Your Render URL
```

2. **Commit and push:**
```bash
git add static/config.js
git commit -m "Update production API URL"
git push
```

3. **Done!** GitHub Pages will automatically update.

## Troubleshooting

### "Cannot connect to server"
- Make sure the backend is running on port 5000
- Check `static/config.js` has the correct API URL
- Check browser console for detailed errors

### Backend won't start
- Verify `.env` file exists with `GEMINI_API_KEY`
- Check all dependencies installed: `pip list`
- Verify port 5000 is not in use

### "Invalid API Key" error
- Get a new key from https://makersuite.google.com/app/apikey
- Make sure there are no spaces in the `.env` file
- Restart the backend after updating `.env`

### Rate limit errors
- Wait a minute and try again
- The limit is 20 requests per minute per IP

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for more deployment options
- Read [SECURITY.md](SECURITY.md) for security best practices
- Read [TESTING.md](TESTING.md) for comprehensive testing guide
- Customize particle settings in `static/script.js`
- Customize colors in `static/style.css`

## Get Help

- Check existing issues: https://github.com/anacondy/live-volcano-ui/issues
- Create a new issue if you're stuck
- Include error messages and screenshots

## What's Included

✅ Beautiful animated particle background
✅ Gemini 2.5 Pro AI integration
✅ Intelligent college website search
✅ Context-aware query understanding
✅ Secure API with rate limiting
✅ Smooth text animations
✅ Mobile responsive
✅ Complete documentation

Enjoy your new AI-powered UI! 🌋✨
