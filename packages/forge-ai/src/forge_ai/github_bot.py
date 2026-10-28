import os
import requests

def post_pr_comment(owner: str, repo: str, pr_number: int, comment_body: str):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not found. Skipping PR comment.")
        return
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
    response = requests.post(url, json={"body": comment_body}, headers=headers)
    response.raise_for_status()
    return response.json()