// Paste this code into script.js
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('background-canvas');
    const ctx = canvas.getContext('2d');
    const inputWrapper = document.querySelector('.input-wrapper');
    const chatInput = document.getElementById('chat-input');
    const feedbackMessage = document.getElementById('feedback-message');
    let width, height;
    const particles = [];
    const particleCount = 500;
    const noiseScale = 0.003;
    const particleSpeed = 0.5;
    const lineOpacity = 0.05;
    let feedbackTimeout;
    const mouse = { x: null, y: null, radius: 100 };
    window.addEventListener('mousemove', (event) => {
        mouse.x = event.x;
        mouse.y = event.y;
    });
    window.addEventListener('mouseout', () => {
        mouse.x = null;
        mouse.y = null;
    });
    const noise = (() => {
        let p = new Uint8Array(512);
        for (let i = 0; i < 256; i++) p[i] = p[i + 256] = Math.floor(Math.random() * 256);

        function fade(t) { return t * t * t * (t * (t * 6 - 15) + 10); }

        function lerp(t, a, b) { return a + t * (b - a); }

        function grad(hash, x, y, z) {
            let h = hash & 15,
                u = h < 8 ? x : y,
                v = h < 4 ? y : h == 12 || h == 14 ? x : z;
            return ((h & 1) == 0 ? u : -u) + ((h & 2) == 0 ? v : -v);
        }
        return {
            noise: function(x, y, z) {
                let X = Math.floor(x) & 255,
                    Y = Math.floor(y) & 255,
                    Z = Math.floor(z) & 255;
                x -= Math.floor(x);
                y -= Math.floor(y);
                z -= Math.floor(z);
                let u = fade(x),
                    v = fade(y),
                    w = fade(z);
                let A = p[X] + Y,
                    AA = p[A] + Z,
                    AB = p[A + 1] + Z,
                    B = p[X + 1] + Y,
                    BA = p[B] + Z,
                    BB = p[B + 1] + Z;
                return lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z), grad(p[BA], x - 1, y, z)), lerp(u, grad(p[AB], x, y - 1, z), grad(p[BB], x - 1, y - 1, z))), lerp(v, lerp(u, grad(p[AA + 1], x, y, z - 1), grad(p[BA + 1], x - 1, y, z - 1)), lerp(u, grad(p[AB + 1], x, y - 1, z - 1), grad(p[BB + 1], x - 1, y - 1, z - 1))));
            }
        }
    })();
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
        }
        update(time) {
            const angle = noise.noise(this.x * noiseScale, this.y * noiseScale, time * 0.0001) * Math.PI * 2;
            let vx = Math.cos(angle) * particleSpeed;
            let vy = Math.sin(angle) * particleSpeed;
            if (mouse.x != null) {
                const dx = this.x - mouse.x;
                const dy = this.y - mouse.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < mouse.radius) {
                    const force = (mouse.radius - distance) / mouse.radius;
                    vx += (dx / distance) * force * 2;
                    vy += (dy / distance) * force * 2;
                }
            }
            this.x += vx;
            this.y += vy;
            if (this.x > width) this.x = 0;
            if (this.x < 0) this.x = width;
            if (this.y > height) this.y = 0;
            if (this.y < 0) this.y = height;
        }
        draw(ctx) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, 1, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function setup() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        updateCanvasColors();
        particles.length = 0;
        for (let i = 0; i < particleCount; i++) { particles.push(new Particle()); }
    }

    function animate(time) {
        const bgColor = getComputedStyle(document.documentElement).getPropertyValue('--background-color').trim();
        const r = parseInt(bgColor.slice(1, 3), 16),
            g = parseInt(bgColor.slice(3, 5), 16),
            b = parseInt(bgColor.slice(5, 7), 16);
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${lineOpacity})`;
        ctx.fillRect(0, 0, width, height);
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--line-color').trim();
        particles.forEach(p => {
            p.update(time);
            p.draw(ctx);
        });
        requestAnimationFrame(animate);
    }

    function updateCanvasColors() {
        const currentLineColor = getComputedStyle(document.documentElement).getPropertyValue('--line-color').trim();
        ctx.fillStyle = currentLineColor;
    }
    chatInput.addEventListener('focus', () => inputWrapper.classList.add('glowing'));
    chatInput.addEventListener('blur', () => inputWrapper.classList.remove('glowing'));

    function applyTextAnimation(element, text, charClass, staggerMs) {
        element.innerHTML = '';
        text.split('').forEach((char, index) => {
            const span = document.createElement('span');
            span.className = charClass;
            span.textContent = char === ' ' ? '\u00A0' : char;
            span.style.animationDelay = `${index * staggerMs}ms`;
            element.appendChild(span);
        });
    }

    function calculateDisplayDuration(text) {
        // Minimum 4 seconds as per requirement
        const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
        // Base formula: ~400ms per word with minimum 4 seconds
        const duration = Math.max(4000, wordCount * 400);
        return duration;
    }

    function showFeedback(message, animationType, duration) {
        clearTimeout(feedbackTimeout);
        if (animationType === 'carved') { applyTextAnimation(feedbackMessage, message, 'carved-char', 50); if (duration) { feedbackTimeout = setTimeout(() => feedbackMessage.innerHTML = '', duration); } } else if (animationType === 'smoky') {
            applyTextAnimation(feedbackMessage, message, 'smoky-char', 30);
            const displayDuration = duration || calculateDisplayDuration(message);
            feedbackTimeout = setTimeout(() => feedbackMessage.innerHTML = '', displayDuration);
        }
    }

    function getStaticBotResponse(message) { const user_message = message.toLowerCase(); let bot_response = "I'm not sure how to respond to that. Try asking about 'themes' or 'creator'."; if (user_message.includes('hello') || user_message.includes('hi')) { bot_response = "Hello there! How can I help you today?"; } else if (user_message.includes('theme') || user_message.includes('color')) { bot_response = "You can change the color theme using the palette icon in the top-right corner!"; } else if (user_message.includes('creator') || user_message.includes('who made you')) { bot_response = "I was created from a creative idea and brought to life with code."; } else if (user_message.includes('awesome') || user_message.includes('cool') || user_message.includes('love this')) { bot_response = "Thank you! I'm glad you like it."; } return bot_response; }
    
    // Clear feedback when user starts typing a new message
    chatInput.addEventListener('input', () => {
        if (chatInput.value.trim() !== '') {
            clearTimeout(feedbackTimeout);
            feedbackMessage.innerHTML = '';
        }
    });
    
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && chatInput.value.trim() !== '') {
            e.preventDefault();
            const userText = chatInput.value;
            chatInput.value = '';
            showFeedback("Thinking...", 'carved');
            setTimeout(() => {
                const botReply = getStaticBotResponse(userText);
                showFeedback(botReply, 'smoky');
            }, 700);
        }
    });
    setup();
    requestAnimationFrame(animate);
    window.addEventListener('resize', setup);
});