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

python affinity_industry_updater.py

3. When prompted, paste your JSON data in the following format:
```json
{
  "org_id": 294274304,
  "Industries_Classification": [
    {
      "Industry": "Emerging Technologies",
      "Sub-Industries": [
        "Augmented reality (AR)",
        "Semiconductors"
      ]
    }
  ]
}```


4. Follow the prompts to confirm the organization and update the industry data.

Updating
The script will automatically check for updates each time it runs. If a new version is available, it will download and install it automatically.
Troubleshooting

If you encounter any issues, try running the script with the debug flag: python affinity_industry_updater.py -d
Make sure your API key is correctly set either in the environment variable or in the config.ini file.
Ensure you have an active internet connection.

## Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request.
## License
MIT License
## Support
If you encounter any problems or have any questions, please open an issue in the GitHub repository.
