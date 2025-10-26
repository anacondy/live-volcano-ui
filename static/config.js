// API Configuration
// Update this file with your deployed backend API URL

const CONFIG = {
    // For local development
    LOCAL_API_URL: 'http://localhost:5000',
    
    // For production - UPDATE THIS with your deployed API URL
    // Examples:
    // - Render: 'https://your-app.onrender.com'
    // - Heroku: 'https://your-app.herokuapp.com'
    // - Cloud Run: 'https://your-service-xxxxx.run.app'
    PRODUCTION_API_URL: 'YOUR_DEPLOYED_API_URL',
    
    // Automatically detect environment
    getApiUrl: function() {
        const isLocal = window.location.hostname === 'localhost' || 
                       window.location.hostname === '127.0.0.1';
        return isLocal ? this.LOCAL_API_URL : this.PRODUCTION_API_URL;
    }
};
