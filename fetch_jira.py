import requests
import json
import os
from requests.auth import HTTPBasicAuth

EMAIL = os.getenv('JIRA_USER_EMAIL')
TOKEN = os.getenv('JIRA_API_TOKEN')
BASE_URL = os.getenv('JIRA_BASE_URL')

def fetch_incidents():
    # Attempt to fetch incidents
    url = f"{BASE_URL}/rest/api/3/search"
    auth = HTTPBasicAuth(EMAIL, TOKEN)
    headers = {"Accept": "application/json"}
    
    # Updated JQL: Fetches issues of type 'Incident'
    query = {
        'jql': 'issuetype = "Incident" ORDER BY created DESC',
        'fields': ['summary', 'status', 'priority', 'created', 'updated']
    }

    try:
        print(f"Connecting to {BASE_URL}...")
        response = requests.request("GET", url, headers=headers, params=query, auth=auth)
        
        # Check if the API call was successful
        if response.status_code == 200:
            data = response.json()
            issues = data.get('issues', [])
            
            # ALWAYS write the file, even if issues is an empty list []
            with open('incidents.json', 'w') as f:
                json.dump(issues, f, indent=4)
            
            print(f"Success! Found {len(issues)} incidents. 'incidents.json' updated.")
            
        else:
            print(f"Jira API Error: {response.status_code}")
            print(f"Details: {response.text}")
            # Optional: Create an empty file so the Git command doesn't fail
            with open('incidents.json', 'w') as f:
                json.dump([], f)

    except Exception as e:
        print(f"Script failed with error: {e}")
        # Ensure the file exists to satisfy the GitHub Action commit step
        if not os.path.exists('incidents.json'):
            with open('incidents.json', 'w') as f:
                json.dump([], f)

if __name__ == "__main__":
    fetch_incidents()
