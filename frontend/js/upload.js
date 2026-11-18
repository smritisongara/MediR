/**
 * MediR AI - Document, Camera & Video Upload Manager
 */

let cameraStream = null;

document.addEventListener('DOMContentLoaded', () => {
  setupDropZone();
  setupSampleButtons();
  setupCamera();
  setupVideoUpload();
});

// 1. Drag and drop file upload
function setupDropZone() {
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('reportFileInput');
  if (!dropZone || !fileInput) return;

  dropZone.addEventListener('click', () => fileInput.click());

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      uploadFile(files[0]);
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      uploadFile(fileInput.files[0]);
    }
  });
}

function uploadFile(file) {
  const statusBox = document.getElementById('uploadStatusBox');
  const progressText = document.getElementById('uploadProgressText');
  
  if (statusBox) statusBox.style.display = 'block';
  if (progressText) progressText.innerText = `Uploading and analyzing ${file.name}...`;

  const formData = new FormData();
  formData.append('file', file);

  fetch('/api/upload', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      sessionStorage.setItem('current_report', JSON.stringify(data));
      window.location.href = `explanation.html?id=${data.report_id}`;
    } else {
      alert(`Upload Error: ${data.error || 'Failed to process document'}`);
      if (statusBox) statusBox.style.display = 'none';
    }
  })
  .catch(err => {
    alert("Connection error occurred while uploading. Please check the backend server.");
    if (statusBox) statusBox.style.display = 'none';
  });
}

// 2. Sample Report Pre-load Buttons for Instant Hackathon Demonstration
function setupSampleButtons() {
  const sampleCbcBtn = document.getElementById('btnSampleCbc');
  const sampleLipidBtn = document.getElementById('btnSampleLipid');
  const samplePrescBtn = document.getElementById('btnSamplePresc');

  if (sampleCbcBtn) {
    sampleCbcBtn.addEventListener('click', () => {
      loadSampleReport('sample_cbc_report.txt', 'Sample CBC Blood Test');
    });
  }

  if (sampleLipidBtn) {
    sampleLipidBtn.addEventListener('click', () => {
      loadSampleReport('sample_lipid_profile.txt', 'Sample Lipid Profile Panel');
    });
  }

  if (samplePrescBtn) {
    samplePrescBtn.addEventListener('click', () => {
      loadSampleReport('sample_prescription.txt', 'Sample Doctor Prescription');
    });
  }
}

function loadSampleReport(filename, title) {
  const statusBox = document.getElementById('uploadStatusBox');
  const progressText = document.getElementById('uploadProgressText');
  if (statusBox) statusBox.style.display = 'block';
  if (progressText) progressText.innerText = `Loading ${title}...`;

  fetch(`/sample_data/${filename}`)
    .then(res => res.text())
    .then(text => {
      return fetch('/api/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sample_text: text, sample_title: title })
      });
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        sessionStorage.setItem('current_report', JSON.stringify(data));
        window.location.href = `explanation.html?id=${data.report_id}`;
      } else {
        alert("Error loading sample: " + data.error);
        if (statusBox) statusBox.style.display = 'none';
      }
    })
    .catch(err => {
      alert("Failed to load sample data file.");
      if (statusBox) statusBox.style.display = 'none';
    });
}

// 3. Live Camera Photo Capture
function setupCamera() {
  const startCamBtn = document.getElementById('btnStartCamera');
  const captureBtn = document.getElementById('btnCapturePhoto');
  const retakeBtn = document.getElementById('btnRetakePhoto');
  const submitCamBtn = document.getElementById('btnSubmitPhoto');
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  const camBox = document.getElementById('cameraBox');

  if (!startCamBtn) return;

  startCamBtn.addEventListener('click', async () => {
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 } },
        audio: false
      });
      video.srcObject = cameraStream;
      camBox.style.display = 'block';
      startCamBtn.style.display = 'none';
    } catch (err) {
      alert("Camera access was denied or is not available on this device.");
    }
  });

  captureBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    video.style.display = 'none';
    canvas.style.display = 'block';
    captureBtn.style.display = 'none';
    retakeBtn.style.display = 'inline-flex';
    submitCamBtn.style.display = 'inline-flex';
  });

  retakeBtn.addEventListener('click', () => {
    video.style.display = 'block';
    canvas.style.display = 'none';
    captureBtn.style.display = 'inline-flex';
    retakeBtn.style.display = 'none';
    submitCamBtn.style.display = 'none';
  });

  submitCamBtn.addEventListener('click', () => {
    const dataUrl = canvas.toDataURL('image/png');
    // Stop camera stream
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }

    const statusBox = document.getElementById('uploadStatusBox');
    if (statusBox) statusBox.style.display = 'block';

    fetch('/api/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ camera_image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        sessionStorage.setItem('current_report', JSON.stringify(data));
        window.location.href = `explanation.html?id=${data.report_id}`;
      } else {
        alert("OCR error on camera photo: " + (data.error || "Please capture a clearer photo."));
        if (statusBox) statusBox.style.display = 'none';
      }
    })
    .catch(() => {
      alert("Error sending camera photo to server.");
      if (statusBox) statusBox.style.display = 'none';
    });
  });
}

// 4. Video Upload Handler
function setupVideoUpload() {
  const videoInput = document.getElementById('videoFileInput');
  const videoSubmitBtn = document.getElementById('btnUploadVideo');
  if (!videoInput || !videoSubmitBtn) return;

  videoSubmitBtn.addEventListener('click', () => {
    if (!videoInput.files || videoInput.files.length === 0) {
      alert("Please select a video file (MP4, WebM, MOV) first.");
      return;
    }

    const file = videoInput.files[0];
    const formData = new FormData();
    formData.append('video', file);

    const resultBox = document.getElementById('videoResultBox');
    const statusText = document.getElementById('videoStatusText');
    if (statusText) statusText.innerText = "Analyzing video instructions and extracting transcript...";
    if (resultBox) resultBox.style.display = 'block';

    fetch('/api/video/analyze', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById('videoTranscriptText').innerText = data.transcript;
        document.getElementById('videoSummaryText').innerText = data.summary;
        const list = document.getElementById('videoKeyPointsList');
        if (list) {
          list.innerHTML = data.key_points.map(pt => `<li class="mb-1">✅ ${pt}</li>`).join('');
        }
        if (statusText) statusText.innerText = "Analysis Completed Successfully!";
      } else {
        alert("Video analysis error: " + data.error);
      }
    })
    .catch(() => alert("Connection error during video upload."));
  });
}
