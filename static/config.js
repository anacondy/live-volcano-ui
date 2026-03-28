// API Configuration
// Update this file with your deployed backend API URL

const CONFIG = {
    // For local development
    LOCAL_API_URL: 'http://localhost:5000',
    
    // For Vercel production - when frontend and backend are hosted together, 
    // we use an empty string so the browser fetches from the same domain (e.g. /api/chat)
    PRODUCTION_API_URL: '',
    
    // Automatically detect environment
    getApiUrl: function() {
        const isLocal = window.location.hostname === 'localhost' || 
                       window.location.hostname === '127.0.0.1';
        // On local, use the Flask dev server port. On Vercel, it uses the current domain seamlessly
        return isLocal ? this.LOCAL_API_URL : this.PRODUCTION_API_URL;
    }
};
