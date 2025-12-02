# Development Environment Setup Guide

This guide will walk you through setting up your development environment for the Broadcast (AI) Transcriber application on Windows PC using Visual Studio Code.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing Python](#installing-python)
3. [Installing Visual Studio Code](#installing-visual-studio-code)
4. [Installing Git](#installing-git)
5. [Cloning the Repository](#cloning-the-repository)
6. [Setting Up Virtual Environment](#setting-up-virtual-environment)
7. [Installing Dependencies](#installing-dependencies)
8. [VS Code Configuration](#vs-code-configuration)
9. [Verifying Installation](#verifying-installation)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- Windows 10 or Windows 11
- Administrator access to install software
- Stable internet connection
- At least 2GB of free disk space

---

## Installing Python

### Step 1: Download Python

1. Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest Python 3.x version (3.8 or higher recommended)
3. Look for the "Download Python 3.x.x" button

### Step 2: Install Python

1. Run the downloaded installer
2. **IMPORTANT**: Check the box "Add Python to PATH" at the bottom of the installer
3. Click "Install Now"
4. Wait for the installation to complete
5. Click "Close" when finished

### Step 3: Verify Python Installation

1. Open Command Prompt (Press `Win + R`, type `cmd`, press Enter)
2. Type the following command and press Enter:
   ```cmd
   python --version
   ```
3. You should see output like: `Python 3.x.x`

4. Also verify pip is installed:
   ```cmd
   pip --version
   ```
5. You should see output like: `pip x.x.x from ...`

---

## Installing Visual Studio Code

### Step 1: Download VS Code

1. Visit: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Click the "Download for Windows" button
3. The stable build will be downloaded

### Step 2: Install VS Code

1. Run the downloaded installer (VSCodeUserSetup-x64-x.x.x.exe)
2. Accept the license agreement
3. Choose installation location (default is fine)
4. **Recommended**: Check these options:
   - ✅ Add "Open with Code" action to Windows Explorer file context menu
   - ✅ Add "Open with Code" action to Windows Explorer directory context menu
   - ✅ Register Code as an editor for supported file types
   - ✅ Add to PATH
5. Click "Install"
6. Click "Finish" when complete

### Step 3: Install VS Code Extensions

1. Open Visual Studio Code
2. Click the Extensions icon in the left sidebar (or press `Ctrl + Shift + X`)
3. Search for and install the following extensions:
   - **Python** (by Microsoft) - Essential for Python development
   - **Pylance** (by Microsoft) - Advanced Python language support
   - **Flask Snippets** (by cstrap) - Flask code snippets
   - **HTML CSS Support** (by ecmel) - HTML and CSS IntelliSense
   - **JavaScript (ES6) code snippets** (by charalampos karypidis) - JS snippets
   - **Live Server** (by Ritwick Dey) - Optional, for quick HTML previews
   - **GitLens** (by GitKraken) - Enhanced Git capabilities

---

## Installing Git

### Step 1: Download Git

1. Visit: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the 64-bit Git for Windows Setup

### Step 2: Install Git

1. Run the installer
2. Use default options, but note these important settings:
   - Default editor: Select "Use Visual Studio Code as Git's default editor"
   - Adjusting PATH: Select "Git from the command line and also from 3rd-party software"
   - HTTPS transport: Use the OpenSSL library
   - Line ending conversions: Checkout Windows-style, commit Unix-style line endings
3. Complete the installation

### Step 3: Configure Git

1. Open Command Prompt or VS Code Terminal
2. Set your name:
   ```cmd
   git config --global user.name "Your Name"
   ```
3. Set your email:
   ```cmd
   git config --global user.email "your.email@example.com"
   ```

---

## Cloning the Repository

### Option 1: Using Command Line

1. Open Command Prompt
2. Navigate to where you want to store the project:
   ```cmd
   cd C:\Users\YourUsername\Documents\Projects
   ```
3. Clone the repository:
   ```cmd
   git clone <repository-url>
   cd PythonVideoStreamTranscriber
   ```

### Option 2: Using VS Code

1. Open VS Code
2. Press `Ctrl + Shift + P` to open Command Palette
3. Type "Git: Clone" and select it
4. Paste the repository URL
5. Choose a folder location
6. Click "Open" when prompted

---

## Setting Up Virtual Environment

### Step 1: Open Project in VS Code

1. Open VS Code
2. File → Open Folder
3. Navigate to the `PythonVideoStreamTranscriber` folder
4. Click "Select Folder"

### Step 2: Open Terminal in VS Code

1. Press `` Ctrl + ` `` (backtick) or go to Terminal → New Terminal
2. Ensure you're in the project root directory

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

This creates a `venv` folder containing the virtual environment.

### Step 4: Activate Virtual Environment

In the VS Code terminal, run:

```cmd
venv\Scripts\activate
```

You should see `(venv)` appear at the beginning of your terminal prompt.

**Note**: If you encounter an execution policy error, run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 5: Select Python Interpreter in VS Code

1. Press `Ctrl + Shift + P`
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `venv` (should show `./venv/Scripts/python.exe`)

---

## Installing Dependencies

With the virtual environment activated, install the required packages:

```cmd
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Werkzeug (WSGI utility library)

### Verify Installation

```cmd
pip list
```

You should see Flask and Werkzeug listed.

---

## VS Code Configuration

### Step 1: Create VS Code Settings

1. Create a `.vscode` folder in your project root (if it doesn't exist)
2. Create a `settings.json` file inside `.vscode`
3. Add the following configuration:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "autopep8",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### Step 2: Create Launch Configuration (Optional)

1. Click the Run icon in the left sidebar (or press `Ctrl + Shift + D`)
2. Click "create a launch.json file"
3. Select "Python" → "Flask"
4. VS Code will create `.vscode/launch.json` with Flask configuration

Example `launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--host=0.0.0.0",
                "--port=5000"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

---

## Verifying Installation

### Step 1: Run the Application

With the virtual environment activated:

```cmd
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### Step 2: Test in Browser

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You should see the Broadcast (AI) Transcriber interface

### Step 3: Test Functionality

1. Enter a YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Click "Start"
3. Verify the video appears and the Stop button is enabled
4. Click "Stop"
5. Verify the video disappears and the Start button is re-enabled

---

## Troubleshooting

### Issue: Python Not Found

**Solution**:
- Ensure Python is added to PATH
- Restart Command Prompt or VS Code
- Reinstall Python with "Add to PATH" checked

### Issue: Cannot Activate Virtual Environment

**Error**: `venv\Scripts\activate : File cannot be loaded because running scripts is disabled`

**Solution**:
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Close and reopen VS Code

### Issue: Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
- Ensure virtual environment is activated (you should see `(venv)` in terminal)
- Run: `pip install -r requirements.txt`
- Verify: `pip list` shows Flask

### Issue: Port Already in Use

**Error**: `Address already in use`

**Solution**:
- Stop any other Flask applications
- Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`
- Or find and kill the process using port 5000:
  ```cmd
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

### Issue: VS Code Not Recognizing Virtual Environment

**Solution**:
1. Press `Ctrl + Shift + P`
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `venv`
4. Restart VS Code

### Issue: Browser Shows 404 Error

**Solution**:
- Ensure the Flask app is running
- Check the terminal for errors
- Verify you're accessing `http://localhost:5000` not `https://`

---

## Next Steps

Once your environment is set up, proceed to [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Running the application
- Debugging techniques
- Development workflow
- Testing procedures

---

## Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Git Documentation](https://git-scm.com/doc)

---

**Need Help?**

If you encounter issues not covered here, please:
1. Check the [DEVELOPMENT.md](DEVELOPMENT.md) guide
2. Review Flask and Python documentation
3. Open an issue in the repository
