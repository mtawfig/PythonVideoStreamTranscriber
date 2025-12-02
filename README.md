# Broadcast (AI) Transcriber

![Logo](static/images/logo.svg)

## Overview

**Broadcast (AI) Transcriber** is a modern Python web application that enables users to watch YouTube videos while displaying live transcriptions. The application provides an intuitive interface for embedding YouTube videos and viewing AI-powered transcriptions in real-time.

## Features

- 🎥 **YouTube Video Embedding**: Simply paste any YouTube URL to start watching
- 🤖 **Real-Time AI Transcription**: Powered by AssemblyAI for accurate speech-to-text
- 🎙️ **Speaker Diarization**: Identifies and labels different speakers in the video
- 📡 **Live Stream Support**: Works with both regular videos and live YouTube streams
- 🔄 **WebSocket Integration**: Real-time transcription streaming as the video plays
- 🎨 **Modern UI/UX**: Clean, responsive design with a professional color palette
- 📱 **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- ✨ **Smooth Animations**: Enhanced user experience with modern transitions and effects
- 📜 **Auto-Scrolling**: Transcription automatically scrolls as new text appears
- ✅ **URL Validation**: Intelligent validation of YouTube URLs before streaming
- 📊 **Status Indicators**: Visual feedback for transcription progress

## Technology Stack

- **Backend**: Flask (Python 3.x) with Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla) with Socket.IO
- **Transcription**: AssemblyAI API
- **Video Processing**: yt-dlp for audio extraction
- **Real-time Communication**: WebSocket (Socket.IO)
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: SVG graphics

## Project Structure

```
PythonVideoStreamTranscriber/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── SETUP.md                    # Development environment setup guide
├── DEVELOPMENT.md              # Development and debugging guide
│
├── templates/
│   └── index.html              # Main application template
│
└── static/
    ├── css/
    │   └── style.css           # Application styles
    ├── js/
    │   └── app.js              # Client-side JavaScript
    └── images/
        └── logo.svg            # Application logo
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A modern web browser
- **AssemblyAI API Key** (get one free at [assemblyai.com](https://www.assemblyai.com/))
- FFmpeg (required by yt-dlp for audio extraction)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PythonVideoStreamTranscriber
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure API Key**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your AssemblyAI API key:
     ```
     ASSEMBLYAI_API_KEY=your_api_key_here
     ```

6. **Install FFmpeg** (if not already installed):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

7. Run the application:
   ```bash
   python app.py
   ```

8. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter YouTube URL**: Paste a valid YouTube video URL (regular video or live stream) in the input field
2. **Click Start**: The application will:
   - Validate the URL
   - Fetch video metadata (title, channel, duration)
   - Embed the video for playback
   - Download audio and start real-time transcription
3. **Watch & Read**:
   - View the video on the left
   - Read the AI-generated transcription on the right as it appears in real-time
   - See speaker labels if multiple speakers are detected
   - Monitor transcription status with the indicator
4. **Auto-Scrolling**: The transcription area automatically scrolls as new text appears
5. **Click Stop**: Stop the video and transcription, reset the interface

## Color Palette

The application uses a carefully selected color palette:

- **Deep Navy** (#0a1128ff) - Primary background
- **Dark Blue** (#001f54ff) - Secondary backgrounds
- **Ocean Blue** (#034078ff) - Accents
- **Bright Teal** (#1282a2ff) - Highlights and CTAs
- **Off White** (#fefcfbff) - Text and light elements

## Documentation

For detailed setup and development instructions, please refer to:

- [SETUP.md](SETUP.md) - Complete development environment setup guide
- [DEVELOPMENT.md](DEVELOPMENT.md) - Debugging and development instructions

## Future Enhancements

- ✅ ~~Real-time AI transcription integration~~ (Implemented with AssemblyAI)
- ✅ ~~Support for live YouTube streams~~ (Implemented)
- ✅ ~~Speaker diarization~~ (Implemented)
- Multi-language transcription support
- Downloadable transcription files (PDF, TXT, SRT)
- Timestamp synchronization with video playback
- User authentication and transcription history
- Customizable transcription settings (language, format)
- Search within transcriptions
- Translation to multiple languages
- Enhanced live stream real-time processing

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ using Flask and modern web technologies**
