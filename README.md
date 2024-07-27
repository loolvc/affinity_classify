# Affinity CRM Industry Updater

This tool updates Industry fields in Affinity CRM. It allows you to easily manage and update industry classifications for organizations in your Affinity CRM instance.

## Features

- Automatically fetches and updates industry data for specified organizations
- Supports multiple industries and sub-industries
- Securely manages API keys
- Auto-updates to the latest version
- Runs in a virtual environment to avoid conflicts with other Python installations

## Prerequisites

- Python 3.6 or higher
- Internet connection

## Installation

### For Mac/Linux Users:

1. Download the `install.sh` script.
2. Open Terminal and navigate to the directory containing the script.
3. Make the script executable: `chmod +x install.sh`
4. Run the installer: `./install.sh`

### For Windows Users:

1. Download the `install.bat` script.
2. Double-click the `install.bat` file to run it.

## Configuration

After installation, you need to set up your Affinity API key. You have two options:

1. Set an environment variable named `AFFINITY_API_KEY` with your API key.
2. Edit the `config.ini` file in the installation directory and replace `{AFFINITY_API_KEY}` with your actual API key.

## Usage

1. Activate the virtual environment:
   - On Mac/Linux: `source affinity_updater_env/bin/activate`
   - On Windows: `affinity_updater_env\Scripts\activate.bat`

2. Run the script:
