@echo off

set REPO=loolvc/affinity_classify
set VENV_NAME=affinity_classify_env
set SCRIPT_NAME=affinity_classify.py

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install it from https://www.python.org/downloads/
    exit /b 1
)

REM Create a virtual environment if it doesn't exist
if not exist %VENV_NAME% (
    python -m venv %VENV_NAME%
    echo Created virtual environment: %VENV_NAME%
) else (
    echo Virtual environment already exists: %VENV_NAME%
)

REM Activate the virtual environment
call %VENV_NAME%\Scripts\activate.bat

REM Upgrade pip
pip install --upgrade pip

REM Install or upgrade required packages
pip install requests configparser

REM Download the latest release
for /f "tokens=2 delims=:" %%a in ('curl -s https://api.github.com/repos/%REPO%/releases/latest ^| findstr "browser_download_url.*py"') do (
    set DOWNLOAD_URL=%%a
    set DOWNLOAD_URL=!DOWNLOAD_URL:"=!
    curl -LO !DOWNLOAD_URL!
)

REM Create config.ini if it doesn't exist
if not exist config.ini (
    echo [Affinity] > config.ini
    echo API_KEY = {AFFINITY_API_KEY} >> config.ini
    echo Created config.ini file. Please update it with your API key.
)

echo Installation complete!
echo To run the script:
echo 1. Activate the virtual environment: %VENV_NAME%\Scripts\activate.bat
echo 2. Run the script: python %SCRIPT_NAME%

pause
