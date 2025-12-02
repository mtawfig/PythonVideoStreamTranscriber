# YouTube Cookies Export Guide

If you encounter videos that fail to download with all client strategies, you may need to export your YouTube cookies. This guide will help you export cookies from your browser.

## Why Do I Need Cookies?

Some YouTube videos have restrictions that require authentication:
- Age-restricted videos
- Member-only content
- Region-locked videos
- Videos with special privacy settings

By exporting your browser cookies, the app can authenticate as if you're logged into YouTube.

## Prerequisites

- You must be logged into YouTube in your browser
- You should be able to watch the video in your browser while logged in

---

## Method 1: Browser Extension (Easiest)

### For Chrome/Edge:

1. **Install Extension**:
   - Go to Chrome Web Store
   - Search for **"Get cookies.txt LOCALLY"**
   - Install the extension

2. **Export Cookies**:
   - Go to `https://www.youtube.com` (make sure you're logged in)
   - Click the extension icon in your toolbar
   - Click "Export" button
   - Save the file as `youtube_cookies.txt`

3. **Place Cookies File**:
   - Move `youtube_cookies.txt` to your project root directory:
     ```
     PythonVideoStreamTranscriber/
     ├── youtube_cookies.txt  ← Here
     ├── app.py
     ├── .env
     └── ...
     ```

4. **Configure .env**:
   - Open your `.env` file
   - Add this line:
     ```
     YOUTUBE_COOKIES_FILE=youtube_cookies.txt
     ```

5. **Restart Flask App**:
   ```bash
   # Stop the app (Ctrl+C)
   python app.py
   ```

### For Firefox:

1. **Install Extension**:
   - Go to Firefox Add-ons
   - Search for **"cookies.txt"** by Lenka Segura
   - Install the add-on

2. **Export Cookies**:
   - Go to `https://www.youtube.com`
   - Click the extension icon
   - Click "Download cookies.txt"
   - Save as `youtube_cookies.txt`

3. **Follow steps 3-5 from Chrome instructions above**

---

## Method 2: Using yt-dlp Command (Advanced)

You can also use yt-dlp's built-in browser cookie extraction:

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Extract cookies from Chrome
yt-dlp --cookies-from-browser chrome --cookies youtube_cookies.txt "https://www.youtube.com"

# Or from Firefox
yt-dlp --cookies-from-browser firefox --cookies youtube_cookies.txt "https://www.youtube.com"

# Or from Edge
yt-dlp --cookies-from-browser edge --cookies youtube_cookies.txt "https://www.youtube.com"
```

Then configure `.env` as shown in Method 1, step 4.

---

## Method 3: Manual Export (Most Reliable)

### Chrome/Edge:

1. **Open Developer Tools**:
   - Go to `https://www.youtube.com`
   - Press `F12` or `Ctrl+Shift+I`

2. **Navigate to Application Tab**:
   - Click "Application" tab
   - In left sidebar: Storage → Cookies → `https://www.youtube.com`

3. **Export All Cookies**:
   - Right-click in the cookies list
   - Select "Clear All"... NO! Don't do that!
   - Actually, manually copy each cookie (this is tedious)

**Note**: Manual export is complex. Use Method 1 or 2 instead.

---

## Cookies File Format

The `youtube_cookies.txt` file should be in Netscape cookie format:

```
# Netscape HTTP Cookie File
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	0	CONSENT	YES+cb
.youtube.com	TRUE	/	FALSE	1234567890	VISITOR_INFO1_LIVE	xxxxx
.youtube.com	TRUE	/	TRUE	1234567890	LOGIN_INFO	xxxxx
```

---

## Testing Cookies

After adding cookies:

1. **Restart Flask app**:
   ```bash
   python app.py
   ```

2. **Look for cookie confirmation** in console:
   ```
   🍪 Using cookies from: youtube_cookies.txt
   ```

3. **Try a restricted video**:
   - Age-restricted videos should now work
   - You should see successful downloads

---

## Security Notes

⚠️ **IMPORTANT SECURITY WARNINGS**:

1. **Never commit cookies to Git**:
   - The `.gitignore` file already excludes `youtube_cookies.txt`
   - Double-check before committing: `git status`

2. **Cookies contain authentication tokens**:
   - Anyone with your cookies can access YouTube as you
   - Don't share your `youtube_cookies.txt` file

3. **Cookies expire**:
   - YouTube cookies typically expire after a few weeks
   - If downloads stop working, re-export cookies

4. **Use cookies only on your personal computer**:
   - Don't upload cookies to servers
   - Don't share cookies with others

---

## Troubleshooting

### "Cookies file not found" message

**Solution**: Make sure the file is in the correct location:
```
PythonVideoStreamTranscriber/
├── youtube_cookies.txt  ← Should be here at root level
├── app.py
└── .env
```

### Still getting 403 errors with cookies

**Possible causes**:
1. **Cookies expired**: Re-export fresh cookies
2. **Wrong format**: Make sure file is in Netscape format
3. **Not logged in**: Make sure you were logged into YouTube when exporting
4. **Video truly restricted**: Some videos can't be downloaded even with cookies

### Cookies not being used

Check your `.env` file:
```bash
# Make sure this line is present and correct
YOUTUBE_COOKIES_FILE=youtube_cookies.txt
```

Restart Flask app after changing `.env`.

---

## Alternative: Download Without Cookies

If you don't want to use cookies, try these alternatives:

1. **Use different videos**:
   - Most public videos don't require cookies
   - Avoid age-restricted content

2. **Test with known-working videos**:
   - Popular music videos
   - Major channel uploads
   - Educational content

3. **Check video accessibility**:
   - Can you watch it without logging in?
   - Try in incognito/private browsing mode

---

## Need Help?

If you're still having issues:

1. Check that you're using the latest yt-dlp: `pip install --upgrade yt-dlp`
2. Try the video in an incognito window (logged out)
3. Check if the video has geographic restrictions
4. Try a different video to verify the app works

---

**Remember**: Most public YouTube videos don't require cookies. Only use this guide if you encounter specific videos that fail with all client strategies.
