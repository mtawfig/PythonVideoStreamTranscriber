from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import re
import os
import threading
import time
from dotenv import load_dotenv
import yt_dlp
import assemblyai as aai

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
socketio = SocketIO(app, cors_allowed_origins="*")

# AssemblyAI Configuration
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = ASSEMBLYAI_API_KEY

# Store active transcription sessions
active_sessions = {}

def is_valid_youtube_url(url):
    """
    Validate if the provided URL is a valid YouTube URL.
    Supports various YouTube URL formats including:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - Live streams
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|live/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|live/|.+\?v=)?([^&=%\?]{11})')

    match = re.match(youtube_regex, url)
    if match:
        return match.group(6)
    return None

def get_video_metadata(video_id):
    """
    Fetch video metadata including title, channel, and live status using yt-dlp.
    """
    try:
        url = f'https://www.youtube.com/watch?v={video_id}'

        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'extractor_args': {
                'youtube': {
                    'skip': ['hls', 'dash'],
                    'player_client': ['ios', 'android'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'X-Youtube-Client-Name': '5',
                'X-Youtube-Client-Version': '19.29.1',
            },
        }

        print(f"Fetching metadata for: {url}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                'title': info.get('title', 'Unknown Title'),
                'channel': info.get('uploader', 'Unknown Channel'),
                'is_live': info.get('is_live', False),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
            }
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        import traceback
        traceback.print_exc()
        return {
            'title': 'Unknown Title',
            'channel': 'Unknown Channel',
            'is_live': False,
            'duration': 0,
            'thumbnail': '',
        }

def download_audio(video_id):
    """
    Download audio from YouTube video for transcription.
    Returns the path to the downloaded audio file.
    Uses multiple client fallback strategies to bypass 403 errors.
    """
    # Create temp directory if it doesn't exist
    if not os.path.exists('temp_audio'):
        os.makedirs('temp_audio')

    url = f'https://www.youtube.com/watch?v={video_id}'
    output_path = f'temp_audio/{video_id}'

    # Try different player clients in order of reliability
    # web and mweb don't require PO tokens as of Dec 2025
    client_strategies = [
        {
            'name': 'web',
            'player_client': ['web'],
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        },
        {
            'name': 'mweb',
            'player_client': ['mweb'],
            'user_agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        },
        {
            'name': 'android_testsuite',
            'player_client': ['android_testsuite'],
            'user_agent': 'com.google.android.youtube/19.29.37 (Linux; U; Android 14) gzip',
        },
        {
            'name': 'ios',
            'player_client': ['ios'],
            'user_agent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
        },
        {
            'name': 'android_embedded',
            'player_client': ['android_embedded'],
            'user_agent': 'com.google.android.youtube/19.29.37 (Linux; U; Android 14) gzip',
        },
    ]

    # Check for cookies file
    cookies_file = os.getenv('YOUTUBE_COOKIES_FILE', 'youtube_cookies.txt')
    use_cookies = os.path.exists(cookies_file)

    for strategy in client_strategies:
        try:
            print(f"\n=== Trying {strategy['name']} client ===")

            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                'outtmpl': output_path + '.%(ext)s',
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                'ignoreerrors': False,
                'extractor_args': {
                    'youtube': {
                        'skip': ['hls', 'dash'],
                        'player_client': strategy['player_client'],
                        'player_skip': ['webpage', 'configs'],
                    }
                },
                'http_headers': {
                    'User-Agent': strategy['user_agent'],
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                },
            }

            # Add cookies if available
            if use_cookies:
                ydl_opts['cookiefile'] = cookies_file
                print(f"🍪 Using cookies from: {cookies_file}")

            print(f"Attempting to download with {strategy['name']} client...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                # Get the actual filename
                if 'requested_downloads' in info and len(info['requested_downloads']) > 0:
                    downloaded_file = info['requested_downloads'][0]['filepath']
                    print(f"✅ Successfully downloaded with {strategy['name']}: {downloaded_file}")

                    # Convert to mp3 if not already and AssemblyAI supports the format
                    if downloaded_file.endswith(('.m4a', '.webm', '.opus')):
                        # AssemblyAI supports these formats, but let's convert to mp3 for consistency
                        mp3_file = f'temp_audio/{video_id}.mp3'
                        print(f"Converting to mp3: {mp3_file}")

                        try:
                            import subprocess
                            result = subprocess.run([
                                'ffmpeg', '-i', downloaded_file,
                                '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k',
                                mp3_file, '-y'
                            ], check=True, capture_output=True, text=True)

                            # Remove original file
                            if os.path.exists(downloaded_file):
                                os.remove(downloaded_file)

                            print(f"✅ Conversion successful: {mp3_file}")
                            return mp3_file
                        except subprocess.CalledProcessError as e:
                            print(f"FFmpeg conversion failed: {e.stderr}")
                            # Return original file if conversion fails - AssemblyAI can handle it
                            print(f"⚠️ Using original format: {downloaded_file}")
                            return downloaded_file
                        except FileNotFoundError:
                            print("⚠️ FFmpeg not found, using original format")
                            return downloaded_file
                    else:
                        return downloaded_file

            # If we get here, check for downloaded files
            for ext in ['m4a', 'webm', 'mp3', 'opus', 'mp4']:
                audio_file = f'temp_audio/{video_id}.{ext}'
                if os.path.exists(audio_file):
                    print(f"✅ Found audio file with {strategy['name']}: {audio_file}")
                    return audio_file

        except Exception as e:
            print(f"❌ {strategy['name']} client failed: {str(e)[:200]}")
            continue

    # All strategies failed
    print(f"\n❌ All download strategies failed for video: {video_id}")
    print("💡 Tip: This video may require authentication. Try:")
    print("   1. Using a different video")
    print("   2. Exporting YouTube cookies and adding them to the app")
    return None

def transcribe_audio(video_id, audio_file, session_id):
    """
    Transcribe audio using AssemblyAI with real-time streaming results.
    """
    try:
        print(f"Starting transcription for video: {video_id}")

        config = aai.TranscriptionConfig(
            speaker_labels=True,  # Enable speaker diarization
            punctuate=True,
            format_text=True,
        )

        transcriber = aai.Transcriber(config=config)

        # Upload and transcribe
        transcript = transcriber.transcribe(audio_file)

        if transcript.status == aai.TranscriptStatus.error:
            socketio.emit('transcription_error', {
                'message': f'Transcription failed: {transcript.error}'
            }, room=session_id)
            return

        # Send complete transcription in chunks for smooth display
        if transcript.utterances:
            for utterance in transcript.utterances:
                if session_id in active_sessions and active_sessions[session_id]['active']:
                    speaker = f"Speaker {utterance.speaker}" if utterance.speaker else ""
                    socketio.emit('transcription_chunk', {
                        'text': utterance.text,
                        'speaker': speaker,
                        'start': utterance.start,
                        'end': utterance.end
                    }, room=session_id)
                    time.sleep(0.1)  # Small delay for smooth display
                else:
                    break
        else:
            # Fallback if no utterances
            if transcript.text:
                socketio.emit('transcription_chunk', {
                    'text': transcript.text,
                    'speaker': '',
                    'start': 0,
                    'end': 0
                }, room=session_id)

        socketio.emit('transcription_complete', {
            'message': 'Transcription completed successfully'
        }, room=session_id)

        print(f"Transcription completed for video: {video_id}")

    except Exception as e:
        print(f"Error during transcription: {e}")
        socketio.emit('transcription_error', {
            'message': f'Transcription error: {str(e)}'
        }, room=session_id)
    finally:
        # Cleanup audio file
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"Cleaned up audio file: {audio_file}")
        except Exception as e:
            print(f"Error cleaning up audio file: {e}")

def transcribe_live_stream(video_id, session_id):
    """
    Transcribe live YouTube stream using AssemblyAI streaming.
    Note: This requires the stream URL which needs to be extracted differently for live streams.
    """
    try:
        print(f"Starting live stream transcription for: {video_id}")

        # For live streams, we need to get the stream URL
        url = f'https://www.youtube.com/watch?v={video_id}'

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],
                    'player_client': ['android', 'web']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info.get('url')

        if not audio_url:
            raise Exception("Could not extract live stream audio URL")

        # Use AssemblyAI streaming transcription
        def on_data(transcript: aai.RealtimeTranscript):
            if not transcript.text:
                return

            if isinstance(transcript, aai.RealtimeFinalTranscript):
                socketio.emit('transcription_chunk', {
                    'text': transcript.text,
                    'speaker': '',
                    'start': 0,
                    'end': 0,
                    'is_live': True
                }, room=session_id)

        def on_error(error: aai.RealtimeError):
            print(f"Live transcription error: {error}")
            socketio.emit('transcription_error', {
                'message': f'Live transcription error: {str(error)}'
            }, room=session_id)

        # Create streaming transcriber
        transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=on_data,
            on_error=on_error,
        )

        transcriber.connect()

        # Note: Full implementation would stream audio chunks to AssemblyAI
        # This is a simplified version - real implementation needs audio streaming
        socketio.emit('transcription_info', {
            'message': 'Live stream transcription started (simplified mode - downloading stream)'
        }, room=session_id)

        # For now, fall back to downloading and transcribing
        # In production, you'd stream the audio directly
        audio_file = download_audio(video_id)
        if audio_file:
            transcriber.close()
            transcribe_audio(video_id, audio_file, session_id)
        else:
            raise Exception("Failed to download live stream audio")

    except Exception as e:
        print(f"Error during live transcription: {e}")
        socketio.emit('transcription_error', {
            'message': f'Live transcription error: {str(e)}'
        }, room=session_id)

@app.route('/')
def index():
    """
    Render the main page of the application.
    """
    return render_template('index.html')

@app.route('/validate_url', methods=['POST'])
def validate_url():
    """
    API endpoint to validate YouTube URLs and fetch metadata.
    """
    data = request.get_json()
    url = data.get('url', '')

    if is_valid_youtube_url(url):
        video_id = extract_video_id(url)
        metadata = get_video_metadata(video_id)

        return jsonify({
            'valid': True,
            'video_id': video_id,
            'embed_url': f'https://www.youtube.com/embed/{video_id}',
            'metadata': metadata
        })
    else:
        return jsonify({
            'valid': False,
            'message': 'Invalid YouTube URL'
        })

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}")

    # Clean up session
    if request.sid in active_sessions:
        active_sessions[request.sid]['active'] = False
        del active_sessions[request.sid]

@socketio.on('start_transcription')
def handle_start_transcription(data):
    """
    Handle transcription start request from client.
    """
    video_id = data.get('video_id')
    is_live = data.get('is_live', False)
    session_id = request.sid

    print(f"Starting transcription for video {video_id}, is_live: {is_live}, session: {session_id}")

    # Store session
    active_sessions[session_id] = {
        'video_id': video_id,
        'active': True,
        'is_live': is_live
    }

    # Start transcription in background thread
    if is_live:
        thread = threading.Thread(
            target=transcribe_live_stream,
            args=(video_id, session_id)
        )
    else:
        # Download audio first
        socketio.emit('transcription_info', {
            'message': 'Downloading audio for transcription...'
        }, room=session_id)

        audio_file = download_audio(video_id)

        if audio_file:
            socketio.emit('transcription_info', {
                'message': 'Audio downloaded. Starting transcription...'
            }, room=session_id)

            thread = threading.Thread(
                target=transcribe_audio,
                args=(video_id, audio_file, session_id)
            )
        else:
            socketio.emit('transcription_error', {
                'message': 'Failed to download audio from video'
            }, room=session_id)
            return

    thread.daemon = True
    thread.start()

@socketio.on('stop_transcription')
def handle_stop_transcription():
    """
    Handle transcription stop request from client.
    """
    session_id = request.sid

    if session_id in active_sessions:
        active_sessions[session_id]['active'] = False
        print(f"Stopped transcription for session: {session_id}")

        socketio.emit('transcription_stopped', {
            'message': 'Transcription stopped'
        }, room=session_id)

if __name__ == '__main__':
    # Create temp directory for audio files
    if not os.path.exists('temp_audio'):
        os.makedirs('temp_audio')

    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
