# Volcanic Flow UI 🌋

An interactive, visually stunning UI featuring a dynamic particle-based animated background with smooth flowing effects. The interface responds to user interactions with elegant animations and provides a captivating user experience.

## ✨ Features

- **Dynamic Particle Animation**: 500+ particles creating mesmerizing flow patterns using Perlin noise
- **Mouse Interaction**: Particles react to mouse movement with a repulsion effect
- **Elegant Input Design**: Glowing input field with smooth focus animations
- **Harry Potter-Style Text Effects**: Messages appear with magical smoky and carved text animations
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

## 🛠️ Technologies Used

- **HTML5**: Structure and canvas element
- **CSS3**: Styling, animations, and responsive design
- **Vanilla JavaScript**: Particle system, animations, and interactions
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

1. Clone the repository:
```bash
git clone https://github.com/anacondy/live-volcano-ui.git
```

2. Open `index.html` in your browser or serve with a local server:
```bash
# Using Python
python -m http.server 8080

# Using Node.js
npx http-server
```

3. Visit `http://localhost:8080` in your browser

## 💬 Usage

1. Click on the input field to activate the glowing effect
2. Type your message and press Enter
3. Watch the magical text animation appear
4. Messages stay visible for at least 4 seconds or until you start typing again
5. Try moving your mouse to interact with the particles!

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
