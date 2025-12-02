/**
 * Broadcast (AI) Transcriber - Main JavaScript
 * Handles YouTube URL validation, video embedding, and UI interactions
 */

// Global variables
let currentVideoId = null;

// DOM Elements
const ytForm = document.getElementById('ytForm');
const ytStreamUrl = document.getElementById('ytstreamurl');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const ytStreaming = document.getElementById('ytstreaming');
const ytVideo = document.getElementById('ytvideo');
const errorMessage = document.getElementById('errorMessage');

/**
 * Initialize event listeners when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Form submit event
    ytForm.addEventListener('submit', handleFormSubmit);

    // Stop button click event
    stopBtn.addEventListener('click', handleStop);

    // Clear error message on input change
    ytStreamUrl.addEventListener('input', function() {
        errorMessage.textContent = '';
        errorMessage.style.display = 'none';
    });
});

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    const url = ytStreamUrl.value.trim();

    // Clear previous error messages
    errorMessage.textContent = '';
    errorMessage.style.display = 'none';

    // Basic client-side validation
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }

    // Validate URL with server
    try {
        const response = await fetch('/validate_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (data.valid) {
            // URL is valid, start streaming
            startStreaming(data.video_id, data.embed_url);
        } else {
            // URL is invalid
            showError(data.message || 'Invalid YouTube URL. Please check and try again.');
        }
    } catch (error) {
        console.error('Error validating URL:', error);
        showError('An error occurred while validating the URL. Please try again.');
    }
}

/**
 * Start streaming the YouTube video
 * @param {string} videoId - YouTube video ID
 * @param {string} embedUrl - YouTube embed URL
 */
function startStreaming(videoId, embedUrl) {
    // Store current video ID
    currentVideoId = videoId;

    // Update button states
    startBtn.disabled = true;
    stopBtn.disabled = false;

    // Create and insert YouTube iframe
    const iframe = document.createElement('iframe');
    iframe.src = embedUrl + '?autoplay=1';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;

    // Clear previous video and insert new one
    ytVideo.innerHTML = '';
    ytVideo.appendChild(iframe);

    // Show streaming section with animation
    ytStreaming.style.display = 'block';

    // Scroll to streaming section
    setTimeout(() => {
        ytStreaming.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Handle stop button click
 */
function handleStop() {
    // Update button states
    startBtn.disabled = false;
    stopBtn.disabled = true;

    // Hide streaming section
    ytStreaming.style.display = 'none';

    // Clear video
    ytVideo.innerHTML = '';

    // Clear video ID
    currentVideoId = null;

    // Clear the input field
    ytStreamUrl.value = '';

    // Clear any error messages
    errorMessage.textContent = '';
    errorMessage.style.display = 'none';

    // Scroll back to top
    window.scrollTo({ behavior: 'smooth', top: 0 });
}

/**
 * Display error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

/**
 * Client-side YouTube URL validation (backup)
 * @param {string} url - URL to validate
 * @returns {boolean} - True if valid YouTube URL
 */
function isValidYouTubeUrl(url) {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)\/(watch\?v=|embed\/|v\/|.+\?v=)?([^&=%\?]{11})/;
    return youtubeRegex.test(url);
}

/**
 * Extract video ID from YouTube URL (backup)
 * @param {string} url - YouTube URL
 * @returns {string|null} - Video ID or null if not found
 */
function extractVideoId(url) {
    const match = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
    return match ? match[1] : null;
}
