# Volcanic Flow UI 🌋 with Gemini AI Integration

An interactive, visually stunning UI featuring a dynamic particle-based animated background with smooth flowing effects, now powered by Google's Gemini 2.5 Pro AI model for intelligent responses about Subodh PG College.

## ✨ Features

- **Gemini 2.5 Pro AI Integration**: Smart, context-aware responses powered by Google's latest AI model
- **College-Specific Intelligence**: Automatically searches Subodh PG College website for exam dates, news, notifications, and more
- **Context-Aware Understanding**: Intelligently interprets queries like "III sem" as "3rd semester"
- **Secure API**: Environment-based configuration, rate limiting, and security headers
- **Dynamic Particle Animation**: 500+ particles creating mesmerizing flow patterns using Perlin noise
- **Mouse Interaction**: Particles react to mouse movement with a repulsion effect
- **Elegant Input Design**: Glowing input field with smooth focus animations
- **Harry Potter-Style Text Effects**: Messages appear with magical smoky and carved text animations
- **Optimized Performance**: Smooth, lag-free text rendering with requestAnimationFrame
- **Responsive Design**: Optimized for desktop and mobile devices (16:9 and 20:9 aspect ratios)
- **Fixed Input Position**: Input bar stays at the bottom, ensuring consistent UX
- **Smart Message Display**: Feedback messages stay visible for at least 4 seconds or until new input begins

## 🚀 Demo

👉 **[Live Demo](https://anacondy.github.io/live-volcano-ui/)**

## 📸 Screenshots

### Desktop View
![Desktop Interface](https://github.com/user-attachments/assets/6ca177c2-d9e4-476d-b210-8372f8a51d3a)

### Desktop with Message
The elegant cursive text animation appears above the input bar:

![Desktop with Message](https://github.com/user-attachments/assets/569a3a3d-fb96-439a-9122-80fdb23a7046)

### Mobile View
![Mobile Interface](https://github.com/user-attachments/assets/37119136-74dd-4b31-970a-fb60ccf14ca2)

### Mobile with Message
On mobile, messages appear above the input to remain visible when the keyboard is active:

![Mobile with Message](https://github.com/user-attachments/assets/6af2d1ae-3d5c-47da-a0b2-123878ee34d2)

## 🤖 AI Features

### Gemini 2.5 Pro Integration
The UI now integrates with Google's Gemini 2.5 Pro model to provide intelligent, context-aware responses specifically tailored for Subodh PG College students.

### What You Can Ask:
- **Exam Information**: "When is the III sem elementary computer application exam?"
- **College News**: "Any new notifications?"
- **Form Status**: "Are exam forms live?"
- **Holidays**: "When is the next holiday?"
- **General Queries**: "How to apply for exams?"

### Smart Features:
- Automatically scrapes and searches the Subodh PG College website (https://www.subodhpgcollege.com/)
- Understands context: "III sem" = "3rd semester"
- Provides short, precise answers
- Formats dates clearly (e.g., "29 Oct, 2025 (1st shift)")
- Caches website data for faster responses

### Security:
- API keys stored securely in environment variables
- Rate limiting (20 requests/minute)
- CORS protection with specific origins
- Input validation and sanitization
- Security headers (XSS, CSRF protection)
- Content length limits

## 🛠️ Technologies Used

- **HTML5**: Structure and canvas element
- **CSS3**: Styling, animations, and responsive design
- **Vanilla JavaScript**: Particle system, animations, and interactions
- **Python Flask**: Backend API server
- **Google Generative AI**: Gemini 2.5 Pro model integration
- **BeautifulSoup4**: Web scraping for college website
- **Perlin Noise Algorithm**: For smooth, natural particle movement
- **Google Fonts**: 'Alex Brush' cursive font for elegant text display

## 🎨 Key Design Elements

### Particle System
- 500 particles with Perlin noise-based movement
- Mouse interaction with repulsion force
- Smooth wrapping at screen edges
- Configurable speed and noise scale

### Text Animations
- **Carved Effect**: Characters appear with scaling and glow
- **Smoky Wind Effect**: Text gracefully fades with blur and movement
- Staggered character animations for smooth entrance

### Responsive Behavior
- Fixed bottom position for input bar
- Feedback messages positioned above input on mobile
- Safe area insets support for modern mobile devices
- Optimized font sizes and spacing for different screen sizes

## 📱 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚦 Getting Started

### Frontend (GitHub Pages)
The frontend is automatically deployed via GitHub Pages:

👉 **[Live Demo](https://anacondy.github.io/live-volcano-ui/)**

### Backend Setup (Required for AI Features)

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

3. **Configure environment variables:**
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_DEBUG=False
PORT=5000
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

4. **Run the backend server:**
```bash
python api/app.py
```

5. **Update frontend configuration:**
Edit `static/config.js` and update the PRODUCTION_API_URL:
```javascript
PRODUCTION_API_URL: 'https://your-deployed-api-url.com'
```

6. **Serve the frontend:**
```bash
python -m http.server 8080
```

7. **Open browser:** http://localhost:8080

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Render (recommended)
- Heroku
- PythonAnywhere
- Google Cloud Run

### GitHub Pages (Frontend)
The frontend is automatically deployed via GitHub Pages:
- Any commits to the main branch automatically update the live site
- Site URL: https://anacondy.github.io/live-volcano-ui/
- To enable: Go to repository Settings → Pages → Source: main branch

**Note:** After deploying your backend API, update `static/config.js` with your production API URL and commit the changes.

## 💬 Usage

1. **Visit the live site**: https://anacondy.github.io/live-volcano-ui/
2. **Ask questions** about Subodh PG College:
   - "When is the III sem elementary computer application exam?"
   - "Are exam forms live?"
   - "What are the latest notifications?"
   - "Show me exam schedule"
3. **Get smart responses** powered by Gemini AI that searches the college website
4. **Watch the magical text animation** appear with smooth rendering
5. **Try moving your mouse** to interact with the particles!

## 🎯 Customization

### Particle Settings
Edit `static/script.js`:
```javascript
const particleCount = 500;      // Number of particles
const noiseScale = 0.003;       // Smoothness of movement
const particleSpeed = 0.5;      // Speed of particles
const lineOpacity = 0.05;       // Trail opacity
```

### Colors and Theme
Edit `static/style.css`:
```css
:root {
    --background-color: #0d1018;
    --line-color: rgba(230, 230, 230, 0.6);
    --accent-color: #EDFF00;
    --text-color: #ffffff;
    --selection-pink: #ff69b4;
}
```

### Message Duration
Edit `static/script.js`:
```javascript
function calculateDisplayDuration(text) {
    const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
    const duration = Math.max(4000, wordCount * 400); // Minimum 4s
    return duration;
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**anacondy**

## 🙏 Acknowledgments

- Inspired by particle flow visualizations
- Perlin noise algorithm for natural movement
- Google Fonts for beautiful typography

---

⭐ If you like this project, please give it a star on GitHub!
