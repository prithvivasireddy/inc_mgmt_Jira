import requests
import json
import os

# Configuration
email = os.getenv('JIRA_USER_EMAIL')
token = os.getenv('JIRA_API_TOKEN')
url = f"{os.getenv('JIRA_BASE_URL')}/rest/api/3/search"

# JQL: Change 'project' to your project key
query = {
    "jql": "project = 'INC' AND issuetype = 'Incident' ORDER BY created DESC",
    "fields": ["summary", "status", "priority", "created", "updated"]
}

response = requests.get(url, params=query, auth=(email, token))

if response.status_code == 200:
    with open('incidents.json', 'w') as f:
        json.dump(response.json(), f)
else:
    print(f"Failed to fetch: {response.status_code}")
