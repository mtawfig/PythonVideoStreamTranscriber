/**
 * Broadcast (AI) Transcriber - Main JavaScript
 * Handles YouTube URL validation, video embedding, real-time transcription via WebSocket
 */

// Global variables
let socket = null;
let currentVideoId = null;
let currentMetadata = null;
let isTranscribing = false;

// DOM Elements
const ytForm = document.getElementById('ytForm');
const ytStreamUrl = document.getElementById('ytstreamurl');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const ytStreaming = document.getElementById('ytstreaming');
const ytVideo = document.getElementById('ytvideo');
const errorMessage = document.getElementById('errorMessage');
const transcriptionTitle = document.getElementById('transcriptionTitle');
const transcriptionStatus = document.getElementById('transcriptionStatus');
const transcriptionBody = document.getElementById('transcriptionBody');

/**
 * Initialize Socket.IO connection and event listeners when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO connection
    initializeSocket();

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
 * Initialize Socket.IO connection and set up event handlers
 */
function initializeSocket() {
    socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    // Transcription info messages
    socket.on('transcription_info', (data) => {
        console.log('Transcription info:', data.message);
        updateStatus(data.message, 'info');
    });

    // Transcription chunks (real-time text)
    socket.on('transcription_chunk', (data) => {
        console.log('Received transcription chunk:', data);
        appendTranscriptionChunk(data);
    });

    // Transcription complete
    socket.on('transcription_complete', (data) => {
        console.log('Transcription complete:', data.message);
        updateStatus('Transcription complete', 'complete');
        isTranscribing = false;
    });

    // Transcription error
    socket.on('transcription_error', (data) => {
        console.error('Transcription error:', data.message);
        updateStatus(`Error: ${data.message}`, 'error');
        showError(data.message);
        isTranscribing = false;
    });

    // Transcription stopped
    socket.on('transcription_stopped', (data) => {
        console.log('Transcription stopped:', data.message);
        isTranscribing = false;
    });
}

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
        updateStatus('Validating YouTube URL...', 'info');

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
            currentMetadata = data.metadata;
            startStreaming(data.video_id, data.embed_url, data.metadata);
        } else {
            // URL is invalid
            showError(data.message || 'Invalid YouTube URL. Please check and try again.');
            updateStatus('Invalid URL', 'error');
        }
    } catch (error) {
        console.error('Error validating URL:', error);
        showError('An error occurred while validating the URL. Please try again.');
        updateStatus('Validation error', 'error');
    }
}

/**
 * Start streaming the YouTube video and transcription
 * @param {string} videoId - YouTube video ID
 * @param {string} embedUrl - YouTube embed URL
 * @param {object} metadata - Video metadata (title, channel, is_live, etc.)
 */
function startStreaming(videoId, embedUrl, metadata) {
    // Store current video ID
    currentVideoId = videoId;
    currentMetadata = metadata;

    // Update button states
    startBtn.disabled = true;
    stopBtn.disabled = false;

    // Update title and channel
    const titleText = `${metadata.title} - ${metadata.channel}`;
    transcriptionTitle.textContent = titleText;

    // Clear previous transcription
    transcriptionBody.innerHTML = '<p class="transcription-text">Starting transcription...</p>';

    // Update status
    updateStatus('Loading video...', 'info');

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

    // Start transcription via WebSocket
    startTranscription(videoId, metadata.is_live);
}

/**
 * Start transcription process via WebSocket
 * @param {string} videoId - YouTube video ID
 * @param {boolean} isLive - Whether the video is a live stream
 */
function startTranscription(videoId, isLive) {
    isTranscribing = true;
    updateStatus('Starting transcription...', 'info');

    // Clear previous transcription
    transcriptionBody.innerHTML = '';

    // Send start transcription event to server
    socket.emit('start_transcription', {
        video_id: videoId,
        is_live: isLive
    });

    console.log(`Started transcription for video ${videoId}, is_live: ${isLive}`);
}

/**
 * Append a transcription chunk to the transcription body
 * @param {object} data - Transcription chunk data
 */
function appendTranscriptionChunk(data) {
    const chunk = document.createElement('div');
    chunk.className = 'transcription-chunk';

    if (data.is_live) {
        chunk.classList.add('live');
    }

    // Add speaker label if available
    if (data.speaker) {
        const speakerLabel = document.createElement('span');
        speakerLabel.className = 'speaker-label';
        speakerLabel.textContent = `${data.speaker}: `;
        chunk.appendChild(speakerLabel);
    }

    // Add transcription text
    const textSpan = document.createElement('span');
    textSpan.textContent = data.text;
    chunk.appendChild(textSpan);

    // Append to transcription body
    transcriptionBody.appendChild(chunk);

    // Auto-scroll to bottom
    autoScroll();

    // Update status
    updateStatus('Transcribing...', 'info');
}

/**
 * Auto-scroll the transcription body to the bottom
 */
function autoScroll() {
    // Smooth scroll to bottom
    transcriptionBody.scrollTop = transcriptionBody.scrollHeight;
}

/**
 * Update the transcription status indicator
 * @param {string} message - Status message
 * @param {string} type - Status type ('info', 'complete', 'error')
 */
function updateStatus(message, type = 'info') {
    const statusIndicator = transcriptionStatus.querySelector('.status-indicator');
    const statusText = transcriptionStatus.querySelector('.status-text');

    // Update text
    statusText.textContent = message;

    // Update indicator class
    statusIndicator.classList.remove('complete', 'error');
    if (type === 'complete') {
        statusIndicator.classList.add('complete');
    } else if (type === 'error') {
        statusIndicator.classList.add('error');
    }
}

/**
 * Handle stop button click
 */
function handleStop() {
    // Update button states
    startBtn.disabled = false;
    stopBtn.disabled = true;

    // Stop transcription if running
    if (isTranscribing && socket) {
        socket.emit('stop_transcription');
        isTranscribing = false;
    }

    // Hide streaming section
    ytStreaming.style.display = 'none';

    // Clear video
    ytVideo.innerHTML = '';

    // Clear video ID and metadata
    currentVideoId = null;
    currentMetadata = null;

    // Clear the input field
    ytStreamUrl.value = '';

    // Clear any error messages
    errorMessage.textContent = '';
    errorMessage.style.display = 'none';

    // Reset transcription area
    transcriptionTitle.textContent = 'Welcome to Broadcast (AI) Transcriber';
    transcriptionBody.innerHTML = '<p class="transcription-text">Transcription will appear here as the video plays...</p>';
    updateStatus('Ready', 'info');

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
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)\/(watch\?v=|embed\/|v\/|live\/|.+\?v=)?([^&=%\?]{11})/;
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

/**
 * Format time in seconds to MM:SS format
 * @param {number} seconds - Time in seconds
 * @returns {string} - Formatted time string
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}
