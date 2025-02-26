# GitHub Main Releases Checker

A **daily-updated** site that displays stable (non-draft, non-pre-release, non-hotfix) GitHub releases in a **responsive table**. The project leverages:

- **Python** + **GitHub Actions** to fetch and filter releases.
- **docs/** folder for hosting via **GitHub Pages**.
- **Responsive** table layout (and optional SCSS if desired) for a pretty display of release data.

---

## How It Works

1. **Daily Fetch & JSON Generation**  
   - A **GitHub Action** runs a Python script each day.  
   - The script retrieves all releases from the specified repositories, **skips** drafts, pre-releases, and hotfixes, then **parses** the data and saves it to `docs/data/releases.json`.

2. **GitHub Pages Hosting**  
   - The `docs/` folder contains a static website.  
   - **GitHub Pages** builds from `/docs`, so the **JSON** file and **HTML** page(s) become publicly available.  
   - The site fetches `data/releases.json` and displays it in a **table**.

---

## Repository Structure

```
.
├─ main.py                # Python script that fetches stable releases
├─ docs/
│  ├─ index.html          # The main HTML page (responsive table layout)
│  ├─ data/
│  │  └─ releases.json    # Generated daily by GitHub Actions
│  ├─ _config.yml         # Jekyll config (if using Jekyll-based Pages)
│  └─ (optionally style.scss or other assets)
├─ .github/
│  └─ workflows/
│      └─ scraper.yml     # GitHub Action for daily JSON generation & commit
├─ requirements.txt       # Python dependencies (e.g., requests)
└─ README.md              # Project documentation
```

1. **`main.py`**  
   - Fetches releases from the GitHub API.  
   - Skips draft/pre-release/hotfix.  
   - Includes `tag_name`, `name`, `html_url`, `published_at`.  
   - Writes JSON to `docs/data/releases.json`.

2. **`docs/`**  
   - **`index.html`**: A responsive web page that fetches and displays the JSON data in a table.  
   - **`data/releases.json`**: The final JSON file with stable releases, updated daily.  
   - **`_config.yml`** (Optional): If you use Jekyll themes or custom Sass.

3. **`.github/workflows/scraper.yml`**  
   - The workflow that runs daily (via cron) or on-demand.  
   - Installs `requests`, runs `main.py`, and commits changes if any.

---

## Setup & Usage

1. **Clone** this repo (or fork it).
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (If there’s no file, just `pip install requests`.)

3. **Edit `main.py`** to list the repositories you want to track:
   ```python
   repos = [
       {"owner": "kedacore", "repo": "keda"},
       {"owner": "istio", "repo": "istio"},
       # add more...
   ]
   ```
   Make sure to include:
   ```python
   "name": release.get("name", "")
   ```
   so the release name is captured.

4. **Run locally** (optional):
   ```bash
   python main.py
   ```
   This generates or updates `docs/data/releases.json`.

5. **GitHub Actions**  
   - The `scraper.yml` workflow is set to **run daily** (via `cron`).  
   - It commits **any new release data** to `docs/data/releases.json`.  
   - Check [Actions tab](../../actions) to see logs or manually trigger the workflow.

6. **GitHub Pages**  
   - Go to **Settings** → **Pages** → Choose `Branch: main / Folder: /docs` → Save.  
   - The site will be published at:  
     ```
     https://<username>.github.io/<repo>/
     ```
   - `data/releases.json` is served at:  
     ```
     https://<username>.github.io/<repo>/data/releases.json
     ```

7. **View the Site**  
   - Open the GitHub Pages URL in your browser to see a **responsive table** of stable releases.  
   - The **Published** column is now **wider** to accommodate longer dates.  
   - The **Name** column is populated with the release name, or a dash (—) if missing.

---

## Customization

- **Rearrange Columns**: In `index.html`, reorder the `<th>` and the corresponding `<td>`.
- **Column Widths**:
  ```css
  table {
    table-layout: fixed;
  }
  th:nth-child(4), td:nth-child(4) {
    width: 30%;
  }
  ```
- **Add SCSS**: Put a `style.scss` in `docs/assets/css`, configure `_config.yml` to compile it, and enjoy **Sass** features.
- **Tailwind / Bootstrap**: Instead of custom CSS, load a CSS framework for a modern design quickly.

---

## Contributing

1. **Fork** this repository.
2. **Create a feature branch**, commit your changes.
3. **Open a Pull Request** describing your enhancements.

---

## License

This project is open source under the [MIT License](LICENSE). Feel free to modify and distribute it as you wish.
