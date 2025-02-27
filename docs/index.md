---
layout: default
title: "Releases Dashboard"
---

<style>
/* Override or augment the theme's CSS here */

/* A simple hero/banner area */
.hero {
  background: #f4f8fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

.hero h1 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.hero p {
  margin: 0;
  color: #666;
}

/* Our table styling (cayman theme doesn't provide many built-in table styles) */
.table-container {
  margin-top: 1rem;
  overflow-x: auto;
}

table.releases-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

table.releases-table th,
table.releases-table td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: left;
}

table.releases-table thead {
  background-color: #468faf; /* a nice teal-ish color */
  color: white;
}

tr:hover {
  background: #f9f9f9;
}

/* Button and input styling (optional) */
.controls {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}
.controls button,
.controls input {
  padding: 0.5rem 0.75rem;
}
</style>

<div class="hero">
  <h1>{{ page.title }}</h1>
  <p>Daily-updated stable releases. Automatically sorted by date (newest first). Search for a repository or a tag. </p>
</div>

<div class="controls">
  <button id="refresh-btn" style="cursor:pointer;">Refresh</button>
  <input type="text" id="search-box" placeholder="Search repo/tag..." />
  <span id="last-updated" style="margin-left:auto; color:#666;"></span>
</div>

<div class="table-container">
  <table class="releases-table" id="release-table">
    <thead>
      <tr>
        <th>Repository</th>
        <th>Tag</th>
        <th>Published</th>
        <th>Link</th>
      </tr>
    </thead>
    <tbody id="release-body">
      <!-- Populated by JS -->
    </tbody>
  </table>
</div>

<script>
let releases = [];

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("refresh-btn").addEventListener("click", loadReleases);
  document.getElementById("search-box").addEventListener("input", handleSearch);

  // Initial load
  loadReleases();
});

async function loadReleases() {
  try {
    const response = await fetch("./data/releases.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} - ${response.statusText}`);
    }
    const data = await response.json();

    // If you set "last_fetched" in your Python script:
    if (data.last_fetched) {
      document.getElementById("last-updated").textContent = 
        "Last updated: " + data.last_fetched;
    }

    // The array is either data (if old approach) or data.releases (if you store last_fetched, etc.)
    releases = data.releases || data;

    // Sort by date descending
    sortByDateDesc(releases);

    renderTable(releases);
  } catch (err) {
    const tbody = document.getElementById("release-body");
    tbody.innerHTML = `<tr><td colspan="4" style="color:red; font-weight:bold;">Error: ${err.message}</td></tr>`;
  }
}

function sortByDateDesc(arr) {
  arr.sort((a, b) => {
    const [dayA, monthA, yearA] = a.published_at.split("-").map(Number);
    const dateA = new Date(yearA, monthA - 1, dayA);

    const [dayB, monthB, yearB] = b.published_at.split("-").map(Number);
    const dateB = new Date(yearB, monthB - 1, dayB);

    return dateB - dateA; // newest first
  });
}

function renderTable(data) {
  const tbody = document.getElementById("release-body");
  tbody.innerHTML = "";

  data.forEach(item => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.owner}/${item.repo}</td>
      <td>${item.tag_name}</td>
      <td>${item.published_at}</td>
      <td><a href="${item.html_url}" target="_blank">View</a></td>
    `;
    tbody.appendChild(row);
  });
}

function handleSearch() {
  const query = document.getElementById("search-box").value.trim().toLowerCase();
  if (!query) {
    renderTable(releases);
    return;
  }
  const filtered = releases.filter(item => {
    const repoFull = (item.owner + "/" + item.repo).toLowerCase();
    const tag = item.tag_name.toLowerCase();
    return repoFull.includes(query) || tag.includes(query);
  });
  renderTable(filtered);
}
</script>
