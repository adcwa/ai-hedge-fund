// Additional JavaScript functionality for the AI Hedge Fund web app
// This file can be used for more complex functionality in the future

// Helper function to format numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Helper function to format percentages
function formatPercentage(num) {
    return (Math.round(num * 10) / 10).toFixed(1) + '%';
}

// Helper function to get color class based on signal type
function getSignalClass(signal) {
    signal = signal.toUpperCase();
    if (signal === 'BULLISH' || signal === 'BUY' || signal === 'COVER') {
        return 'bullish';
    } else if (signal === 'BEARISH' || signal === 'SELL' || signal === 'SHORT') {
        return 'bearish';
    } else if (signal === 'NEUTRAL' || signal === 'HOLD') {
        return 'neutral';
    }
    return '';
}

// Function to create a toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Export functions for use in other scripts
window.appHelpers = {
    formatNumber,
    formatPercentage,
    getSignalClass,
    showToast
}; 