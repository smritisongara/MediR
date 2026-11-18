/**
 * MediR AI - Report History & Data Management
 */

document.addEventListener('DOMContentLoaded', () => {
  loadReportsHistory();
});

function loadReportsHistory() {
  const container = document.getElementById('historyReportsContainer');
  if (!container) return;

  fetch('/api/reports')
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        renderReports(data.reports);
      }
    })
    .catch(() => {
      container.innerHTML = '<div class="alert alert-danger">Failed to load reports history.</div>';
    });
}

function renderReports(reports) {
  const container = document.getElementById('historyReportsContainer');
  const countBadge = document.getElementById('reportCountBadge');
  if (countBadge) countBadge.innerText = `${reports.length} Reports`;

  if (reports.length === 0) {
    container.innerHTML = `
      <div class="text-center py-5">
        <i class="bi bi-file-earmark-medical display-1 text-muted"></i>
        <h4 class="mt-3">No Medical Reports Yet</h4>
        <p class="text-muted">Upload your first lab test, doctor note, or prescription to view explanations here.</p>
        <a href="upload.html" class="btn btn-medir btn-medir-primary mt-2">
          <i class="bi bi-cloud-arrow-up"></i> Upload Now
        </a>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th>Report Title</th>
            <th>Upload Date</th>
            <th>Abnormal Values</th>
            <th>Status</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          ${reports.map(r => `
            <tr>
              <td>
                <div class="fw-bold">${r.original_filename}</div>
                <div class="small text-muted">${r.file_type ? r.file_type.toUpperCase() : 'DOC'} File</div>
              </td>
              <td>${r.upload_date}</td>
              <td>
                ${r.abnormal_count > 0 
                  ? `<span class="status-badge status-badge-high">⚠️ ${r.abnormal_count} Flagged</span>` 
                  : `<span class="status-badge status-badge-normal">✅ All Normal</span>`}
              </td>
              <td><span class="badge bg-success">Processed</span></td>
              <td class="text-end">
                <a href="explanation.html?id=${r.report_id}" class="btn btn-sm btn-outline-primary me-2">
                  <i class="bi bi-eye"></i> View
                </a>
                <button onclick="confirmDeleteReport(${r.report_id})" class="btn btn-sm btn-outline-danger">
                  <i class="bi bi-trash"></i> Delete
                </button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

function confirmDeleteReport(reportId) {
  if (confirm(`Are you sure you want to permanently delete Report #${reportId}? This will remove all associated explanations and stored files.`)) {
    fetch(`/api/reports/${reportId}`, {
      method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Report deleted successfully.");
        loadReportsHistory();
      } else {
        alert("Delete failed: " + data.error);
      }
    })
    .catch(() => alert("Error communicating with server."));
  }
}
