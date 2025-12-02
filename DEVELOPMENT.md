# Development and Debugging Guide

This guide covers running, debugging, and developing the Broadcast (AI) Transcriber application on Windows using Visual Studio Code.

## Table of Contents

1. [Running the Application](#running-the-application)
2. [Debugging in VS Code](#debugging-in-vs-code)
3. [Development Workflow](#development-workflow)
4. [Code Structure](#code-structure)
5. [Common Development Tasks](#common-development-tasks)
6. [Testing](#testing)
7. [Performance Optimization](#performance-optimization)
8. [Best Practices](#best-practices)
9. [Common Issues](#common-issues)

---

## Running the Application

### Method 1: Using Terminal (Recommended for Quick Testing)

1. **Open VS Code Terminal** (`` Ctrl + ` ``)

2. **Activate Virtual Environment**:
   ```cmd
   venv\Scripts\activate
   ```

3. **Run the Application**:
   ```cmd
   python app.py
   ```

4. **Access the Application**:
   - Open browser: `http://localhost:5000`

5. **Stop the Application**:
   - Press `Ctrl + C` in the terminal

### Method 2: Using VS Code Debugger (Recommended for Development)

1. **Open Run and Debug Panel**: Press `Ctrl + Shift + D`

2. **Select Configuration**: "Python: Flask"

3. **Start Debugging**: Press `F5` or click the green play button

4. **Access the Application**: `http://localhost:5000`

5. **Stop Debugging**: Press `Shift + F5`

### Method 3: Using VS Code Run Button

1. Open `app.py`
2. Click the "Run Python File" button (▶️) in the top-right corner
3. The app will start in the integrated terminal

---

## Debugging in VS Code

### Setting Breakpoints

1. **Add Breakpoint**:
   - Click in the left margin (gutter) next to a line number
   - Or place cursor on line and press `F9`
   - A red dot appears indicating a breakpoint

2. **Common Breakpoint Locations**:
   - `app.py:17` - Inside `is_valid_youtube_url()` function
   - `app.py:30` - Inside `extract_video_id()` function
   - `app.py:43` - Inside `/validate_url` route

### Debug Controls

- **F5**: Start/Continue debugging
- **F10**: Step Over (execute current line)
- **F11**: Step Into (enter function)
- **Shift + F11**: Step Out (exit function)
- **Shift + F5**: Stop debugging
- **Ctrl + Shift + F5**: Restart debugging

### Debug Views

1. **Variables Panel**:
   - Shows local and global variables
   - Inspect variable values during execution

2. **Watch Panel**:
   - Add expressions to monitor
   - Right-click variable → "Add to Watch"

3. **Call Stack**:
   - Shows function execution order
   - Click to jump to specific call

4. **Debug Console**:
   - Execute Python code at breakpoint
   - Example: Type `url` to see URL value

### Debugging Frontend (JavaScript)

1. **Browser DevTools**:
   - Press `F12` in browser
   - Sources tab → Find `app.js`
   - Click line number to set breakpoint

2. **Console Logging**:
   - Check browser console (`F12` → Console)
   - Application already has console.error for errors

3. **Network Tab**:
   - Monitor AJAX requests to `/validate_url`
   - Check request/response data

---

## Development Workflow

### Standard Workflow

1. **Start Development Session**:
   ```cmd
   cd PythonVideoStreamTranscriber
   code .
   venv\Scripts\activate
   ```

2. **Make Changes**:
   - Edit files in VS Code
   - Flask auto-reloads when files change (debug mode)

3. **Test Changes**:
   - Refresh browser to see updates
   - Check terminal for errors

4. **Commit Changes**:
   ```cmd
   git add .
   git commit -m "Description of changes"
   git push
   ```

### Hot Reload (Auto-Restart)

Flask's debug mode automatically reloads when you save files:

```python
# Already configured in app.py
app.run(debug=True, host='0.0.0.0', port=5000)
```

**What triggers reload**:
- ✅ Python files (.py)
- ✅ Template files (.html)
- ❌ Static files (CSS, JS) - requires browser refresh

---

## Code Structure

### Backend (Flask)

#### `app.py` - Main Application

```python
# Key Functions:

is_valid_youtube_url(url)
# Purpose: Validates YouTube URL format
# Returns: Boolean
# Usage: Called by /validate_url endpoint

extract_video_id(url)
# Purpose: Extracts video ID from YouTube URL
# Returns: String (video ID) or None
# Usage: Called after validation succeeds

@app.route('/')
# Purpose: Serves main page
# Returns: Rendered template

@app.route('/validate_url', methods=['POST'])
# Purpose: API endpoint for URL validation
# Accepts: JSON with 'url' field
# Returns: JSON with validation result
```

### Frontend

#### `templates/index.html` - Main Template

Structure:
- `<nav class="navbar">` - Top navigation
- `<div class="form-section">` - URL input form
- `<div id="ytstreaming">` - Video and transcription container

#### `static/js/app.js` - Client-Side Logic

```javascript
// Key Functions:

handleFormSubmit(event)
// Purpose: Processes form submission
// Validates URL and calls API

startStreaming(videoId, embedUrl)
// Purpose: Displays video and transcription
// Updates UI state

handleStop()
// Purpose: Stops video and resets UI
// Clears all data

showError(message)
// Purpose: Displays error messages to user
```

#### `static/css/style.css` - Styles

CSS Custom Properties:
```css
:root {
    --color-primary: #0a1128ff;
    --color-secondary: #001f54ff;
    --color-accent: #034078ff;
    --color-highlight: #1282a2ff;
    --color-light: #fefcfbff;
}
```

---

## Common Development Tasks

### Adding a New Route

1. **Define Route in app.py**:
```python
@app.route('/new-endpoint', methods=['GET', 'POST'])
def new_endpoint():
    # Your logic here
    return jsonify({'message': 'Success'})
```

2. **Test the Route**:
   - Use browser: `http://localhost:5000/new-endpoint`
   - Or use Postman/cURL for API testing

### Modifying the UI

1. **Edit HTML** (`templates/index.html`):
   - Make changes
   - Save file
   - Refresh browser

2. **Edit CSS** (`static/css/style.css`):
   - Make changes
   - Save file
   - Hard refresh browser (`Ctrl + Shift + R`)

3. **Edit JavaScript** (`static/js/app.js`):
   - Make changes
   - Save file
   - Hard refresh browser (`Ctrl + Shift + R`)

### Changing Color Scheme

Edit CSS custom properties in `style.css`:

```css
:root {
    --color-primary: #your-color;
    --color-secondary: #your-color;
    /* etc. */
}
```

### Adding Dependencies

1. **Activate Virtual Environment**:
   ```cmd
   venv\Scripts\activate
   ```

2. **Install Package**:
   ```cmd
   pip install package-name
   ```

3. **Update requirements.txt**:
   ```cmd
   pip freeze > requirements.txt
   ```

---

## Testing

### Manual Testing Checklist

#### URL Validation Testing

- [ ] Valid YouTube URL (watch format)
  - Test: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
  - Expected: Video loads successfully

- [ ] Valid YouTube URL (short format)
  - Test: `https://youtu.be/dQw4w9WgXcQ`
  - Expected: Video loads successfully

- [ ] Invalid URL
  - Test: `https://example.com`
  - Expected: Error message displayed

- [ ] Empty URL
  - Test: Click Start without entering URL
  - Expected: Error message displayed

#### UI/UX Testing

- [ ] Start button disables after clicking
- [ ] Stop button enables after video loads
- [ ] Stop button resets everything correctly
- [ ] Video section appears/disappears smoothly
- [ ] Transcription text displays correctly

#### Responsive Testing

- [ ] Desktop view (1920x1080)
- [ ] Tablet view (768x1024)
- [ ] Mobile view (375x667)
- [ ] Test form layout on small screens
- [ ] Test video grid on small screens

### Browser Console Testing

1. Open Developer Tools (`F12`)
2. Check Console for errors
3. Check Network tab for failed requests
4. Verify JavaScript loads correctly

### Testing Different YouTube URLs

```
Valid URLs to Test:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
- https://www.youtube.com/embed/VIDEO_ID
- https://www.youtube.com/watch?v=VIDEO_ID&t=30s

Invalid URLs to Test:
- https://www.youtube.com/
- https://vimeo.com/123456
- https://example.com
- Not a URL at all
- (empty string)
```

---

## Performance Optimization

### Backend Optimization

1. **Enable Caching** (for production):
```python
from flask import Flask
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

2. **Gzip Compression** (for production):
```python
from flask_compress import Compress
Compress(app)
```

### Frontend Optimization

1. **Minify CSS/JS** (for production):
   - Use tools like `uglify-js` and `cssnano`

2. **Optimize Images**:
   - Use SVG for logo (already implemented)
   - Compress any PNG/JPG assets

3. **Lazy Loading**:
   - Already implemented (video loads only when needed)

---

## Best Practices

### Python (Backend)

1. **Follow PEP 8**:
   - Use 4 spaces for indentation
   - Use snake_case for functions and variables
   - Maximum line length: 79 characters

2. **Add Docstrings**:
```python
def function_name(param):
    """
    Brief description.

    Args:
        param (type): Description

    Returns:
        type: Description
    """
    pass
```

3. **Error Handling**:
```python
try:
    # Code that might fail
    result = risky_operation()
except SpecificException as e:
    # Handle error
    return jsonify({'error': str(e)}), 400
```

### JavaScript (Frontend)

1. **Use Meaningful Variable Names**:
```javascript
// Good
const youtubeUrlInput = document.getElementById('ytstreamurl');

// Avoid
const x = document.getElementById('ytstreamurl');
```

2. **Add Comments**:
```javascript
// Validate URL before submitting to server
if (!url) {
    showError('Please enter a YouTube URL');
    return;
}
```

3. **Error Handling**:
```javascript
try {
    const response = await fetch('/validate_url', { ... });
    // Handle response
} catch (error) {
    console.error('Error:', error);
    showError('An error occurred');
}
```

### CSS (Styling)

1. **Use CSS Custom Properties**:
   - Already implemented for colors
   - Easy to maintain and modify

2. **Mobile-First Approach**:
   - Base styles for mobile
   - Media queries for larger screens

3. **Organize Sections**:
   - Group related styles
   - Add comments for sections

---

## Common Issues

### Issue: Changes Not Reflecting

**Symptoms**: Code changes don't appear in browser

**Solutions**:
1. Hard refresh browser: `Ctrl + Shift + R`
2. Clear browser cache
3. Check if file is saved (white dot on tab means unsaved)
4. For CSS/JS: Disable browser cache in DevTools (F12 → Network → Disable cache)

### Issue: Flask Not Auto-Reloading

**Symptoms**: Have to manually restart Flask after changes

**Solutions**:
1. Ensure debug mode is enabled in `app.py`
2. Check terminal for syntax errors
3. Restart Flask manually: `Ctrl + C`, then `python app.py`

### Issue: Template Not Found Error

**Symptoms**: `TemplateNotFound: index.html`

**Solutions**:
1. Verify `templates` folder exists
2. Ensure `index.html` is inside `templates` folder
3. Check file name spelling (case-sensitive on some systems)

### Issue: Static Files Not Loading

**Symptoms**: CSS/JS not loading, 404 errors in console

**Solutions**:
1. Verify folder structure: `static/css/`, `static/js/`
2. Check file paths in HTML: `{{ url_for('static', filename='...') }}`
3. Clear browser cache

### Issue: CORS Errors

**Symptoms**: AJAX requests blocked by browser

**Solutions**:
```python
# Add to app.py if needed
from flask_cors import CORS
CORS(app)
```

---

## VS Code Keyboard Shortcuts

### Essential Shortcuts

- `Ctrl + P` - Quick file open
- `Ctrl + Shift + P` - Command palette
- `Ctrl + B` - Toggle sidebar
- `` Ctrl + ` `` - Toggle terminal
- `Ctrl + /` - Toggle comment
- `Alt + Up/Down` - Move line up/down
- `Shift + Alt + Up/Down` - Copy line up/down
- `Ctrl + D` - Select next occurrence
- `Ctrl + F` - Find in file
- `Ctrl + Shift + F` - Find in all files
- `Ctrl + H` - Replace in file

### Python Specific

- `F5` - Start debugging
- `Shift + F5` - Stop debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into

---

## Additional Tools

### Recommended VS Code Extensions for Advanced Development

1. **REST Client** - Test API endpoints from VS Code
2. **Python Docstring Generator** - Auto-generate docstrings
3. **Error Lens** - Inline error highlighting
4. **Better Comments** - Enhanced comment styling
5. **Bracket Pair Colorizer** - Visualize bracket pairs

### External Tools

1. **Postman** - API testing
2. **Chrome DevTools** - Frontend debugging
3. **Git GUI** (optional) - GitKraken, SourceTree

---

## Next Steps

### Phase 2 Features (Future Development)

1. **Real-time Transcription**:
   - Integrate with speech-to-text API
   - WebSocket for live updates

2. **User Authentication**:
   - User accounts
   - Transcription history

3. **Database Integration**:
   - Store transcriptions
   - SQLite or PostgreSQL

4. **Enhanced Features**:
   - Download transcriptions
   - Multiple language support
   - Transcription editing

---

## Resources

### Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)
- [Python Documentation](https://docs.python.org/3/)
- [MDN Web Docs](https://developer.mozilla.org/)

### Learning Resources

- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Real Python](https://realpython.com/)
- [CSS Tricks](https://css-tricks.com/)
- [JavaScript.info](https://javascript.info/)

---

## Getting Help

If you encounter issues:

1. **Check Console/Terminal**: Look for error messages
2. **Search Documentation**: Flask and Python docs are comprehensive
3. **Google the Error**: Include "Flask" or "Python" in search
4. **Check Stack Overflow**: Many common issues are already answered
5. **Review Code**: Use debugging techniques from this guide

---

**Happy Coding!** 🚀
