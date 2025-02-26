import os
import requests
from datetime import datetime

BASE_URL = "https://api.github.com"

repos = [
    {"owner": "kedacore", "repo": "keda"},
    {"owner": "istio", "repo": "istio"},
    {"owner" : "argoproj", "repo": "argo-cd"},
    # add new repos here following the syntax
]

def get_latest_release(owner, repo):
    """Fetch the latest release from GitHub for a given repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/releases"
    headers = {}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes

    releases = response.json()
    if not releases:
        return None
    
    for release in releases:
        if release["draft"]:
            continue
        if release["prerelease"]:
            continue
        if "hotfix" in release["tag_name"].lower() or "hotfix" in (release["name"] or "").lower():
             continue

        published_str = release["published_at"]
        try:
            published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
            published_date_formatted = published_dt.strftime("%d-%m-%Y")
        except ValueError:
            published_date_formatted = published_str

        return {
            "tag_name": release["tag_name"],
            "html_url": release["html_url"],
            "published_at": published_date_formatted
        }

    return None

def main():
    for item in repos:
        result = get_latest_release(item["owner"], item["repo"])
        if result:
            print(f"{item['owner']}/{item['repo']}")
            print(f"  - tag: {result['tag_name']}")
            print(f"  - URL: {result['html_url']}")
            print(f"  - published: {result['published_at']}")
            print()
        else:
            print(f"No releases found for {item['owner']}/{item['repo']}\n")

if __name__ == "__main__":
    main()
