import requests

def github_clone_command(repo_url: str):
    print(f"🐙 Sending request to ingest GitHub repo: {repo_url}...")
    try:
        res = requests.post("http://localhost:8000/api/github/analyze-url", json={"repo_url": repo_url})
        if res.status_code == 200:
            data = res.json()
            print(f"✨ Successfully cloned {data['owner']}/{data['repo']}!")
        else:
            print(f"❌ Error: {res.text}")
    except Exception as e:
        print(f"❌ Failed to connect to ONGISA API: {e}")