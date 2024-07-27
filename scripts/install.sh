#!/bin/bash

# Set variables
REPO="yourusername/your-repo-name"
VENV_NAME="affinity_updater_env"
SCRIPT_NAME="affinity_industry_updater.py"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it from https://www.python.org/downloads/"
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv $VENV_NAME
    echo "Created virtual environment: $VENV_NAME"
else
    echo "Virtual environment already exists: $VENV_NAME"
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install or upgrade required packages
pip install requests configparser

# Download the latest release
LATEST_RELEASE_URL=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep "browser_download_url.*py" | cut -d : -f 2,3 | tr -d \")
curl -LO $LATEST_RELEASE_URL

# Create config.ini if it doesn't exist
if [ ! -f "config.ini" ]; then
    echo "[Affinity]" > config.ini
    echo "API_KEY = {AFFINITY_API_KEY}" >> config.ini
    echo "Created config.ini file. Please update it with your API key."
fi

echo "Installation complete!"
echo "To run the script:"
echo "1. Activate the virtual environment: source $VENV_NAME/bin/activate"
echo "2. Run the script: python $SCRIPT_NAME"
