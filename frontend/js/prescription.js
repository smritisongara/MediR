/**
 * MediR AI - Prescription Scanner & Explainer
 */

document.addEventListener('DOMContentLoaded', () => {
  setupPrescriptionUpload();
  setupSamplePrescription();
});

function setupPrescriptionUpload() {
  const form = document.getElementById('prescriptionUploadForm');
  const fileInput = document.getElementById('prescFileInput');

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        uploadPrescriptionFile(fileInput.files[0]);
      }
    });
  }
}

function setupSamplePrescription() {
  const sampleBtn = document.getElementById('btnLoadSamplePresc');
  if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
      fetch('/sample_data/sample_prescription.txt')
        .then(res => res.text())
        .then(text => {
          fetch('/api/prescription', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prescription_text: text })
          })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              renderPrescriptionResults(data);
            }
          });
        });
    });
  }
}

function uploadPrescriptionFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const statusEl = document.getElementById('prescStatusText');
  if (statusEl) statusEl.innerText = `Analyzing prescription ${file.name}...`;

  fetch('/api/prescription', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      renderPrescriptionResults(data);
    } else {
      alert("Prescription analysis error: " + (data.error || "Failed to parse"));
    }
  })
  .catch(() => alert("Connection error uploading prescription."));
}

function renderPrescriptionResults(data) {
  const resultsCard = document.getElementById('prescriptionResultsCard');
  if (resultsCard) resultsCard.style.display = 'block';

  // Medicines List
  const medsContainer = document.getElementById('medicinesContainer');
  if (medsContainer) {
    const meds = data.medicines || [];
    medsContainer.innerHTML = meds.map(m => `
      <div class="col-md-6 mb-3">
        <div class="p-3 border rounded-3 h-100" style="background-color: var(--bg-card-subtle);">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <h5 class="fw-bold text-primary mb-0">${m.medicine_name}</h5>
            <span class="badge bg-secondary">${m.class}</span>
          </div>
          <div class="text-muted small mb-2">Purpose: ${m.purpose}</div>
          <p class="small fw-semibold mb-1">Written Instruction: <span class="text-dark">${m.instruction_in_prescription}</span></p>
          <div class="alert alert-info py-1 px-2 small mb-0">${m.patient_guidance}</div>
        </div>
      </div>
    `).join('');
  }

  // Instructions
  const instList = document.getElementById('prescInstructionsList');
  if (instList && data.instructions) {
    const instructions = Array.isArray(data.instructions) ? data.instructions : data.instructions.split('\n');
    instList.innerHTML = instructions.map(i => `<li class="mb-1">💧 ${i}</li>`).join('');
  }

  // Precautions
  const precEl = document.getElementById('prescPrecautionsBox');
  if (precEl) {
    precEl.innerText = data.precautions || "Always verify prescription instructions with a licensed pharmacist.";
  }
}
