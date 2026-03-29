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
        mouse.x = event.clientX;
        mouse.y = event.clientY;
    }, { passive: true });

    window.addEventListener('mouseout', () => {
        mouse.x = null;
        mouse.y = null;
    }, { passive: true });

    // Touch support for mobile interaction
    window.addEventListener('touchmove', (event) => {
        if (event.touches.length > 0) {
            mouse.x = event.touches[0].clientX;
            mouse.y = event.touches[0].clientY;
        }
    }, { passive: true });

    window.addEventListener('touchend', () => {
        mouse.x = null;
        mouse.y = null;
    }, { passive: true });
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
        update(time, deltaTime) {
            const timeScale = deltaTime / 16.666; // Normalize to 60fps equivalent speed
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
            this.x += vx * timeScale;
            this.y += vy * timeScale;

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

    let cachedBgColor = '';
    let cachedRgba = '';
    let cachedLineColor = '';

    function updateCanvasColors() {
        const style = getComputedStyle(document.body);
        const bgColor = style.getPropertyValue('--background-color').trim();
        if (bgColor !== cachedBgColor) {
            cachedBgColor = bgColor;
            // Parse hex color if possible, fallback to black
            let r = 13,
                g = 16,
                b = 24; // Default ocean/dark
            if (bgColor.startsWith('#')) {
                r = parseInt(bgColor.slice(1, 3), 16) || r;
                g = parseInt(bgColor.slice(3, 5), 16) || g;
                b = parseInt(bgColor.slice(5, 7), 16) || b;
            } else if (bgColor.startsWith('rgb')) {
                const rgb = bgColor.match(/\d+/g);
                if (rgb && rgb.length >= 3) {
                    r = parseInt(rgb[0]);
                    g = parseInt(rgb[1]);
                    b = parseInt(rgb[2]);
                }
            }
            cachedRgba = `rgba(${r}, ${g}, ${b}, ${lineOpacity})`;
        }
        cachedLineColor = style.getPropertyValue('--line-color').trim();
        ctx.fillStyle = cachedLineColor;
    }

    // Observe theme changes on body to update colors efficiently
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                updateCanvasColors();
            }
        });
    });
    observer.observe(document.body, { attributes: true });

    function setup(initParticles = true) {
        const dpr = window.devicePixelRatio || 1;
        width = window.innerWidth;
        height = window.innerHeight;

        canvas.width = width * dpr;
        canvas.height = height * dpr;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';

        ctx.scale(dpr, dpr);

        updateCanvasColors();
        if (initParticles) {
            particles.length = 0;
            for (let i = 0; i < particleCount; i++) { particles.push(new Particle()); }
        }
    }

    let lastTime = 0;

    function animate(time) {
        if (!lastTime) lastTime = time;
        // Run physics and canvas drawing without relying on 60FPS lock
        const deltaTime = Math.min(time - lastTime, 50); // Cap delta to 50ms to prevent huge jumps if tab was inactive
        lastTime = time;

        ctx.fillStyle = cachedRgba;
        ctx.fillRect(0, 0, width, height);
        ctx.fillStyle = cachedLineColor;
        particles.forEach(p => {
            p.update(time, deltaTime);
            p.draw(ctx);
        });
        requestAnimationFrame(animate);
    }
    chatInput.addEventListener('focus', () => inputWrapper.classList.add('glowing'));
    chatInput.addEventListener('blur', () => inputWrapper.classList.remove('glowing'));

    // Global Keydown: Auto-focus chat input when user starts typing (unless already focused or pressing hotkeys)
    document.addEventListener('keydown', (e) => {
        // Ignore if focus is already in input, or if user is pressing Ctrl/Alt/Meta, or non-printable keys
        if (
            document.activeElement === chatInput ||
            e.ctrlKey || e.altKey || e.metaKey ||
            e.key.length > 1 // Things like 'Enter', 'Shift', 'Backspace'
        ) {
            return;
        }

        chatInput.focus();
    });

    function applyTextAnimation(element, text, charClass, staggerMs) {
        element.innerHTML = '';
        const chars = text.split('');
        const fragment = document.createDocumentFragment();

        chars.forEach((char, index) => {
            const span = document.createElement('span');
            span.className = charClass;
            span.textContent = char === ' ' ? '\u00A0' : char;
            span.style.animationDelay = `${index * staggerMs}ms`;
            fragment.appendChild(span);
        });

        element.appendChild(fragment);
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
        if (animationType === 'carved') {
            applyTextAnimation(feedbackMessage, message, 'carved-char', 50);
            if (duration) {
                feedbackTimeout = setTimeout(() => feedbackMessage.innerHTML = '', duration);
            }
        } else if (animationType === 'smoky') {
            applyTextAnimation(feedbackMessage, message, 'smoky-char', 30);
            const displayDuration = duration || calculateDisplayDuration(message);
            feedbackTimeout = setTimeout(() => feedbackMessage.innerHTML = '', displayDuration);
        }
    }

    // API Configuration - using config.js
    const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.getApiUrl() : 'http://localhost:5000';
    const REQUEST_TIMEOUT_MS = 30000;

    function mapApiIssueToMessage(status, backendMessage) {
        if (status === 400) {
            return backendMessage || 'That request format looks invalid. Please try a shorter, clearer question.';
        }
        if (status === 401 || status === 403) {
            return 'The API rejected this request due to access rules. Please check server credentials/config.';
        }
        if (status === 404) {
            return 'Chat endpoint was not found. Please verify the deployment routes and API path.';
        }
        if (status === 408) {
            return 'The request timed out. Please retry with a shorter message.';
        }
        if (status === 429) {
            return 'Too many requests right now. Please wait a few seconds and try again.';
        }
        if (status >= 500) {
            return backendMessage || 'The server is having trouble right now. Please try again in a moment.';
        }
        return backendMessage || 'Sorry, the API request failed. Please try again.';
    }

    async function getBotResponse(message) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            let data = null;
            try {
                data = await response.json();
            } catch (parseError) {
                data = null;
            }

            if (!response.ok) {
                const backendMessage = data && (data.error || data.response);
                return mapApiIssueToMessage(response.status, backendMessage);
            }

            if (data && data.degraded) {
                return data.response || 'The assistant is in temporary fallback mode. Please try again shortly.';
            }

            if (data && data.response) {
                return data.response;
            }

            return 'The API response was empty. Please try again.';
        } catch (error) {
            clearTimeout(timeoutId);
            console.error('API Error:', error);

            if (error.name === 'AbortError') {
                return 'The API took too long to respond. Please try again.';
            }

            if (!navigator.onLine) {
                return 'You appear to be offline. Please check your internet connection.';
            }

            if (error.message && error.message.includes('Failed to fetch')) {
                return "I'm having trouble connecting to the server. Please make sure the backend API is running.";
            }

            return 'Unexpected API error occurred. Please retry in a moment.';
        }
    }

    // Clear feedback when user starts typing a new message
    chatInput.addEventListener('input', () => {
        if (chatInput.value.trim() !== '') {
            clearTimeout(feedbackTimeout);
            feedbackMessage.innerHTML = '';
        }
    });

    chatInput.addEventListener('keydown', async(e) => {
        if (e.key === 'Enter' && chatInput.value.trim() !== '') {
            e.preventDefault();
            const userText = chatInput.value;
            chatInput.value = '';

            // Blur the input to dismiss the keyboard on mobile
            chatInput.blur();
            chatInput.disabled = true; // Disable input while processing

            showFeedback("Thinking...", 'carved');

            try {
                const botReply = await getBotResponse(userText);
                showFeedback(botReply, 'smoky');
            } catch (error) {
                showFeedback("Sorry, something went wrong. Please try again.", 'smoky');
            } finally {
                chatInput.disabled = false;
                // Don't auto-focus to prevent keyboard from reopening on mobile
            }
        }
    });
    setup();
    requestAnimationFrame(animate);

    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            setup(false);
        }, 100);
    });
});