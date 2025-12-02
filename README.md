# Broadcast (AI) Transcriber

![Logo](static/images/logo.svg)

## Overview

**Broadcast (AI) Transcriber** is a modern Python web application that enables users to watch YouTube videos while displaying live transcriptions. The application provides an intuitive interface for embedding YouTube videos and viewing AI-powered transcriptions in real-time.

## Features

- 🎥 **YouTube Video Embedding**: Simply paste any YouTube URL to start watching
- 📝 **Live Transcription Display**: View transcriptions alongside the video (AI transcription coming in future phases)
- 🎨 **Modern UI/UX**: Clean, responsive design with a professional color palette
- 📱 **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- ✨ **Smooth Animations**: Enhanced user experience with modern transitions and effects
- ✅ **URL Validation**: Intelligent validation of YouTube URLs before streaming

## Technology Stack

- **Backend**: Flask (Python 3.x)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
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

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter YouTube URL**: Paste a valid YouTube video URL in the input field
2. **Click Start**: The Start button will validate and begin streaming the video
3. **Watch & Read**: View the video on the left and transcription on the right
4. **Click Stop**: Stop the video and reset the interface

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

- Real-time AI transcription integration
- Support for live YouTube streams
- Multi-language transcription support
- Downloadable transcription files
- User authentication and history
- Customizable transcription settings

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
