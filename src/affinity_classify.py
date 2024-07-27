import requests
import json
import base64
import argparse
import logging
import os
import configparser
import sys

BASE_URL = 'https://api.affinity.co'
INDUSTRY_FIELD_ID = 808056
CONFIG_FILE = 'config.ini'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_api_key():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    # Try to get the API key from environment variable first
    api_key = os.environ.get('AFFINITY_API_KEY')
    
    # If not in environment, try to get from config file
    if not api_key:
        if 'Affinity' in config and 'API_KEY' in config['Affinity']:
            api_key = config['Affinity']['API_KEY']
        
        # If the config file contains the placeholder, prompt the user
        if not api_key or api_key == '{AFFINITY_API_KEY}':
            api_key = input("Enter your Affinity API key: ")
            
            # Save the entered API key to the config file
            if 'Affinity' not in config:
                config['Affinity'] = {}
            config['Affinity']['API_KEY'] = api_key
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
    
    if not api_key:
        raise ValueError("Affinity API key not found. Please set it in config.ini or as an environment variable.")
    
    return api_key

def configure_logging(debug=False, verbose=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

def make_request(method, url, **kwargs):
    api_key = get_api_key()
    auth_header = base64.b64encode(f':{api_key}'.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json'
    }
    logger.debug(f"Making {method} request to {url}")
    response = requests.request(method, url, headers=headers, **kwargs)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    return response

def get_organization_name(org_id):
    response = make_request('GET', f'{BASE_URL}/organizations/{org_id}')
    if response.status_code == 200:
        return response.json()['name']
    else:
        logger.error(f"Error fetching organization: {response.status_code}")
        return None

def get_fields_values(org_id):
    response = make_request('GET', f'{BASE_URL}/field-values', params={'organization_id': org_id})
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Error fetching field values: {response.status_code}")
        return None
    
def delete_field_value(field_value_id):
    response = make_request('DELETE', f'{BASE_URL}/field-values/{field_value_id}')
    if response.status_code == 200:
        logger.info(f"Deleted field value: {field_value_id}")
    else:
        logger.error(f"Error deleting field value: {response.status_code}")

def create_field_value(org_id, field_id, value):
    data = {
        "field_id": field_id,
        "entity_id": org_id,
        "value": value
    }
    response = make_request('POST', f'{BASE_URL}/field-values', json=data)
    if response.status_code == 200:
        logger.info(f"Created new field value: {value}")
    else:
        logger.error(f"Error creating field value: {response.status_code}")

def auto_update():
    current_version = "1.0.0"  # Update this manually when you release a new version
    repo = "yourusername/your-repo-name"
    response = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")
    if response.status_code == 200:
        latest_version = response.json()["tag_name"]
        if latest_version > current_version:
            print(f"A new version ({latest_version}) is available. Updating...")
            
            # Download the new version
            download_url = response.json()["assets"][0]["browser_download_url"]
            new_script = requests.get(download_url).content
            
            # Replace the current script with the new one
            with open(__file__, 'wb') as script_file:
                script_file.write(new_script)
            
            print("Update complete. Restarting script...")
            
            # Restart the script
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            print("You're running the latest version.")
    else:
        print("Unable to check for updates.")

def main(debug=False, verbose=False):
    configure_logging(debug, verbose)
    auto_update()

    print("Please paste the JSON data for the organization and industries.")
    print("Press Enter twice when you're done:")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    
    user_input = "\n".join(lines)
    
    try:
        data = json.loads(user_input)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        print(f"Invalid JSON input. Please check your data and try again.")
        return

    org_id = data['org_id']
    industries = data['Industries_Classification']

    # Get organization name and confirm
    org_name = get_organization_name(org_id)
    if not org_name:
        return

    print(f"Organization Name: {org_name}")
    confirm = input("Is this the correct organization? (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return

   # Verify field name
    fields_response = make_request('GET', f'{BASE_URL}/fields')
    if fields_response.status_code == 200:
        fields = fields_response.json()
        industry_field = next((field for field in fields if field['id'] == INDUSTRY_FIELD_ID), None)
        if industry_field:
            field_name = industry_field['name']
            if field_name != 'Industry':
                print(f"Warning: The field name is '{field_name}', not 'Industry'.")
                confirm = input("Do you want to proceed? (y/n): ").lower()
                if confirm != 'y':
                    print("Operation cancelled.")
                    return
        else:
            logger.error(f"Field with ID {INDUSTRY_FIELD_ID} not found")
            return
    else:
        logger.error(f"Error fetching fields: {fields_response.status_code}")
        return

    # Check existing values
    all_field_values = get_fields_values(org_id)
    if all_field_values:
        existing_industry_values = [value for value in all_field_values if value['field_id'] == INDUSTRY_FIELD_ID]
        if existing_industry_values:
            print("Existing Industry values:")
            for value in existing_industry_values:
                print(f"- {value['value']}")
            confirm = input("Do you want to replace these values? (y/n): ").lower()
            if confirm != 'y':
                print("Operation cancelled.")
                return

            # Delete existing values
            for value in existing_industry_values:
                delete_field_value(value['id'])
        else:
            print("No existing Industry values found.")
    else:
        logger.error("Failed to retrieve field values.")
        return
    
    # Create new values
    for industry in industries:
        create_field_value(org_id, INDUSTRY_FIELD_ID, industry['Industry'])
        for sub_industry in industry['Sub-Industries']:
            create_field_value(org_id, INDUSTRY_FIELD_ID, sub_industry)

    print("Industry values have been updated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Affinity CRM Industry fields")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    main(debug=args.debug, verbose=args.verbose)
