import requests
import json
import os
from requests.auth import HTTPBasicAuth

# These variables will be pulled from GitHub Secrets
EMAIL = os.getenv('JIRA_USER_EMAIL')
TOKEN = os.getenv('JIRA_API_TOKEN')
BASE_URL = os.getenv('JIRA_BASE_URL')

def fetch_incidents():
    # JQL: Finds all issues in your project of type 'Incident'
    # Change 'project = "YOUR_PROJECT_KEY"' to your actual project key
    jql_query = 'issuetype = "Incident" ORDER BY created DESC'
    
    url = f"{BASE_URL}/rest/api/3/search"
    
    auth = HTTPBasicAuth(EMAIL, TOKEN)
    
    headers = {
        "Accept": "application/json"
    }

    query = {
        'jql': jql_query,
        'maxResults': 50,
        'fields': ['summary', 'status', 'priority', 'created', 'updated']
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    if response.status_code == 200:
        data = response.json()
        # Save results to a file that the frontend will read
        with open('incidents.json', 'w') as f:
            json.dump(data['issues'], f, indent=4)
        print("Successfully updated incidents.json")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_incidents()
