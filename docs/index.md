---
layout: default
title: "Releases"
---

<style>
@media (min-width: 768px) {
  .page-content {
    max-width: 1200px !important;
    margin: 0 auto;
  }
}

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

.table-container {
  margin-top: 1rem;
  overflow-x: auto; /* allows horizontal scroll if columns exceed container width */
}

table.releases-table {
  width: 100%;
  table-layout: fixed; /* enforce column widths below */
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

/* Force each column to a certain width % (sum <= 100%) */
table.releases-table thead th:nth-child(1),
table.releases-table tbody td:nth-child(1) {
  width: 30%; 
}
table.releases-table thead th:nth-child(2),
table.releases-table tbody td:nth-child(2) {
  width: 15%;
}
table.releases-table thead th:nth-child(3),
table.releases-table tbody td:nth-child(3) {
  width: 15%;
}
table.releases-table thead th:nth-child(4),
table.releases-table tbody td:nth-child(4) {
  width: 40%;
}

table.releases-table th,
table.releases-table td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: left;
  word-break: break-word; /* wrap long text instead of overflowing */
  vertical-align: top;
}

table.releases-table thead {
  background-color: #574b90; /* a nice teal-ish color */
  color: #fff;
}

tr:hover {
  background: #f9f9f9;
}

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

    if (data.last_fetched) {
      document.getElementById("last-updated").textContent = 
        "Last updated: " + data.last_fetched;
    }

    releases = data.releases || data;
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
