# GitHub Main Releases Checker

A simple Python script that checks the latest **main** (non-draft, non-pre-release, non-hotfix) release of specified GitHub repositories.

## Features

- Skips **draft** and **pre-release** versions  
- Skips releases labeled "**hotfix**"  
- Shows only day, month, and year (DD-MM-YYYY) for the published date  

## Requirements

- Python 3.7 or higher  
- [Requests](https://pypi.org/project/requests/) (install via `pip install requests`)

## Usage

1. **Clone or download** this repository.
2. **Install dependencies**:
   ```bash
   pip install requests
   ```
3. **Edit `main.py`** to add or remove repositories in the `repos` list:
   ```python
   repos = [
       {"owner": "kedacore", "repo": "keda"},
       {"owner": "istio", "repo": "istio"},
       # Add more repositories here...
   ]
   ```
4. **Run the script**:
   ```bash
   python main.py
   ```
5. **Output** example:
   ```
   Repo: kedacore/keda
     - Release Tag: v2.8.0
     - Release Name: KEDA 2.8
     - URL: https://github.com/kedacore/keda/releases/tag/v2.8.0
     - Published: 15-02-2023

   Repo: istio/istio
     - Release Tag: 1.17.0
     - Release Name: Istio 1.17
     - URL: https://github.com/istio/istio/releases/tag/1.17.0
     - Published: 18-02-2023
   ```

## How It Works

1. **Retrieves** all releases from the GitHub API for each repository.  
2. **Skips** releases if they are drafts, pre-releases, or contain "hotfix" in their name or tag.  
3. **Returns** the first valid (latest) release.  

## Date Format

The date is displayed in **DD-MM-YYYY** format. You can change it in the script by editing:

```python
published_date_formatted = published_dt.strftime("%d-%m-%Y")
```

## License

This project is open source under the [MIT License](LICENSE). Feel free to modify and share it.