import os
import json
import requests
from datetime import datetime

BASE_URL = "https://api.github.com"

# specify tools you want to follow
repos = [
    {"owner": "kubernetes", "repo": "kubernetes"},
    {"owner": "kedacore", "repo": "keda"},
    {"owner": "istio", "repo": "istio"},
    {"owner": "argoproj", "repo": "argo-cd"},
    {"owner": "hashicorp", "repo": "terraform"},
    {"owner": "hashicorp", "repo": "terraform-provider-azurerm"},
    {"owner": "microsoft", "repo": "terraform-provider-azuredevops"},
    {"owner": "elastic", "repo": "elasticsearch"},
    {"owner": "kubernetes-sigs", "repo": "kubebuilder"},
    {"owner": "kubernetes-sigs", "repo": "kustomize"},
    {"owner": "8gears", "repo": "n8n-helm-chart"},
]

def get_latest_main_release(owner, repo):
    """Fetch the first stable release from GitHub for a given repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/releases"
    response = requests.get(url)
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

        published_dt = datetime.strptime(release["published_at"], "%Y-%m-%dT%H:%M:%SZ")
        published_date = published_dt.strftime("%d-%m-%Y")

        return {
            "tag_name": release["tag_name"],
            "name": release.get("name", ""),
            "html_url": release["html_url"],
            "published_at": published_date
        }

    return None

def main():
    result_data = []
    for item in repos:
        owner = item["owner"]
        repo = item["repo"]
        release_info = get_latest_main_release(owner, repo)
        if release_info:
            result_data.append({
                "owner": owner,
                "repo": repo,
                **release_info
            })
        else:
            result_data.append({
                "owner": owner,
                "repo": repo,
                "tag_name": "N/A",
                "name": "No main release found",
                "html_url": "#",
                "published_at": "-"
            })

    output = {
        "last_fetched": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "releases": result_data
    }
    
    # Ensure data directory exists
    os.makedirs("docs/data", exist_ok=True)
    with open("docs/data/releases.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()

