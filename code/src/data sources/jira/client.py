import json
import os
import requests
from typing import Dict, List, Optional

class JiraClient:
    """Client for interacting with Jira API."""
    
    def __init__(self, base_url: str, username: str, api_token: str):
        self.base_url = base_url
        self.auth = (username, api_token)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    def get_issue(self, issue_key: str) -> Dict:
        """Retrieve a Jira issue by its key."""
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_issue(self, project_key: str, issue_type: str, summary: str, description: str) -> Dict:
        """Create a new Jira issue."""
        url = f"{self.base_url}/rest/api/2/issue"
        payload = {
            "fields": {
                "project": {"key": project_key},
                "issuetype": {"name": issue_type},
                "summary": summary,
                "description": description
            }
        }
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def load_templates(self) -> Dict:
        """Load Jira templates from JSON file."""
        template_path = os.path.join(os.path.dirname(__file__), "data", "jira_templates.json")
        with open(template_path, "r") as f:
            return json.load(f)
