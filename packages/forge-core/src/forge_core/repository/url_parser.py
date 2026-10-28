import re

def parse_github_url(url: str) -> tuple[str, str]:
    pattern = r"github\.com/([^/]+)/([^/\s#]+)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f"Invalid GitHub repository URL: {url}")
    owner, repo = match.groups()
    return owner, repo.removesuffix(".git")