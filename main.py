import os
import requests

BASE_URL = "https://api.github.com"

repos = [
    {"owner": "kedacore", "repo": "keda"},
    {"owner": "istio", "repo": "istio"},
    {"owner" : "argoproj", "repo": "argo-cd"},
]

def get_latest_release(owner, repo):
    """Fetch the latest release from GitHub for a given repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/releases"
    headers = {}
    # if token:
    #     headers["Authorization"] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes

    data = response.json()
    if not data:
        # If no releases found
        return None
    
    # data[0] is typically the most recent release in GitHub's response
    latest = data[0]  
    
    # Some repos might mark a "pre-release" at index 0, so you might want
    # to loop until you find the first stable release if that’s your goal.
    
    return {
        "tag_name": latest["tag_name"],
        "name": latest.get("name", ""),
        "html_url": latest["html_url"],
        "published_at": latest["published_at"],
        "is_prerelease": latest["prerelease"]
    }

def main():
    for item in repos:
        result = get_latest_release(item["owner"], item["repo"])
        if result:
            print(f"Repo: {item['owner']}/{item['repo']}")
            print(f"  - Release Tag: {result['tag_name']}")
            print(f"  - Release Name: {result['name']}")
            print(f"  - URL: {result['html_url']}")
            print(f"  - Published: {result['published_at']}")
            print(f"  - Pre-release?: {result['is_prerelease']}")
            print()
        else:
            print(f"No releases found for {item['owner']}/{item['repo']}\n")

if __name__ == "__main__":
    main()
