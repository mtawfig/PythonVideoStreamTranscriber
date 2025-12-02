from flask import Flask, render_template, jsonify, request
import re

app = Flask(__name__)

def is_valid_youtube_url(url):
    """
    Validate if the provided URL is a valid YouTube URL.
    Supports various YouTube URL formats including:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    match = re.match(youtube_regex, url)
    if match:
        return match.group(6)
    return None

@app.route('/')
def index():
    """
    Render the main page of the application.
    """
    return render_template('index.html')

@app.route('/validate_url', methods=['POST'])
def validate_url():
    """
    API endpoint to validate YouTube URLs.
    """
    data = request.get_json()
    url = data.get('url', '')

    if is_valid_youtube_url(url):
        video_id = extract_video_id(url)
        return jsonify({
            'valid': True,
            'video_id': video_id,
            'embed_url': f'https://www.youtube.com/embed/{video_id}'
        })
    else:
        return jsonify({
            'valid': False,
            'message': 'Invalid YouTube URL'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
