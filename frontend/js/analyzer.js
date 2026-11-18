/**
 * MediR AI - Medical Problem & Report Analyzer Controller
 */

let cameraStream = null;
let currentSummaryToSpeak = "";
let analyzerVoiceRec = null;

document.addEventListener('DOMContentLoaded', () => {
  setupSampleButtons();
  setupWrittenInput();
  setupPdfUpload();
  setupCamera();
  setupVoiceInput();
  setupVideoUpload();
  setupAudioControls();
});

// 1. Quick Sample Loaders (CBC & Lipid Profile)
function setupSampleButtons() {
  const cbcBtn = document.getElementById('btnLoadSampleCBC');
  const lipidBtn = document.getElementById('btnLoadSampleLipid');

  if (cbcBtn) {
    cbcBtn.addEventListener('click', () => {
      fetch('/sample_data/sample_cbc_report.txt')
        .then(res => res.text())
        .then(text => {
          document.getElementById('writtenInputText').value = text;
          submitAnalysis({ text: text, title: "Sample CBC Blood Test (Elevated WBC)" });
        });
    });
  }

  if (lipidBtn) {
    lipidBtn.addEventListener('click', () => {
      fetch('/sample_data/sample_lipid_profile.txt')
        .then(res => res.text())
        .then(text => {
          document.getElementById('writtenInputText').value = text;
          submitAnalysis({ text: text, title: "Sample Lipid Profile Panel" });
        });
    });
  }
}

// 2. Tab A: Written Input
function setupWrittenInput() {
  const submitBtn = document.getElementById('btnSubmitWritten');
  const textarea = document.getElementById('writtenInputText');

  if (submitBtn && textarea) {
    submitBtn.addEventListener('click', () => {
      const text = textarea.value.trim();
      if (!text) {
        alert("Please enter medical symptoms or paste report text.");
        return;
      }
      submitAnalysis({ text: text, title: "Written Medical Assessment", input_type: "written" });
    });
  }
}

// 3. Tab B: PDF Document Upload
function setupPdfUpload() {
  const dropZone = document.getElementById('pdfDropZone');
  const fileInput = document.getElementById('pdfFileInput');
  const submitBtn = document.getElementById('btnSubmitPdf');

  if (!dropZone || !fileInput) return;

  dropZone.addEventListener('click', () => fileInput.click());

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
      handlePdfFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      handlePdfFile(fileInput.files[0]);
    }
  });

  function handlePdfFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    showLoader(true);

    fetch('/api/analyzer/process', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      showLoader(false);
      if (data.success && data.simplification) {
        renderAnalysisResults(data.simplification);
      } else {
        alert("PDF Analysis error: " + (data.error || "Failed to process PDF"));
      }
    })
    .catch(() => {
      showLoader(false);
      alert("Network error processing PDF.");
    });
  }
}

// 4. Tab C: Camera & Photo with OCR Review
function setupCamera() {
  const startBtn = document.getElementById('btnStartCamera');
  const captureBtn = document.getElementById('btnCapturePhoto');
  const retakeBtn = document.getElementById('btnRetakePhoto');
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  const box = document.getElementById('cameraBox');
  const reviewText = document.getElementById('ocrReviewText');
  const submitOcrBtn = document.getElementById('btnSubmitOcr');
  const photoInput = document.getElementById('photoFileInput');

  if (!startBtn) return;

  startBtn.addEventListener('click', async () => {
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 } },
        audio: false
      });
      video.srcObject = cameraStream;
      box.style.display = 'block';
      startBtn.style.display = 'none';
      captureBtn.style.display = 'inline-flex';
    } catch (err) {
      alert("Camera access denied or device does not have a camera.");
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

    // Simulate OCR extraction into review textarea
    const dataUrl = canvas.toDataURL('image/png');
    showLoader(true);
    fetch('/api/analyzer/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ camera_image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
      showLoader(false);
      if (data.success) {
        reviewText.value = data.extracted_text;
        renderAnalysisResults(data.simplification);
      }
    })
    .catch(() => showLoader(false));
  });

  retakeBtn.addEventListener('click', () => {
    video.style.display = 'block';
    canvas.style.display = 'none';
    captureBtn.style.display = 'inline-flex';
    retakeBtn.style.display = 'none';
  });

  if (photoInput) {
    photoInput.addEventListener('change', () => {
      if (photoInput.files.length > 0) {
        const formData = new FormData();
        formData.append('file', photoInput.files[0]);
        showLoader(true);
        fetch('/api/analyzer/process', { method: 'POST', body: formData })
          .then(res => res.json())
          .then(data => {
            showLoader(false);
            if (data.success) {
              reviewText.value = data.extracted_text;
              renderAnalysisResults(data.simplification);
            }
          })
          .catch(() => showLoader(false));
      }
    });
  }

  submitOcrBtn.addEventListener('click', () => {
    const text = reviewText.value.trim();
    if (!text) {
      alert("Review text is empty.");
      return;
    }
    submitAnalysis({ text: text, title: "Verified Document Photo Text", input_type: "photo" });
  });
}

// 5. Tab D: Voice Input (Review & Correct before Analysis)
function setupVoiceInput() {
  const micBtn = document.getElementById('btnVoiceMic');
  const statusEl = document.getElementById('voiceStatus');
  const waveBox = document.getElementById('voiceSoundWave');
  const transcriptEdit = document.getElementById('voiceTranscriptEdit');
  const submitVoiceBtn = document.getElementById('btnSubmitVoice');

  if (!micBtn) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    statusEl.innerText = "Speech recognition is not available in this browser. Please type in Tab A.";
    micBtn.disabled = true;
    return;
  }

  analyzerVoiceRec = new SpeechRecognition();
  analyzerVoiceRec.continuous = false;
  analyzerVoiceRec.interimResults = true;

  let listening = false;

  analyzerVoiceRec.onstart = () => {
    listening = true;
    statusEl.innerText = "Listening... Speak your symptoms or question.";
    micBtn.classList.add('listening');
    if (waveBox) waveBox.classList.add('listening');
  };

  analyzerVoiceRec.onresult = (e) => {
    let transcript = '';
    for (let i = e.resultIndex; i < e.results.length; ++i) {
      transcript += e.results[i][0].transcript;
    }
    transcriptEdit.value = transcript;
  };

  analyzerVoiceRec.onerror = (e) => {
    listening = false;
    micBtn.classList.remove('listening');
    if (waveBox) waveBox.classList.remove('listening');
    statusEl.innerText = `Microphone notice: ${e.error}. Tap to try again.`;
  };

  analyzerVoiceRec.onend = () => {
    listening = false;
    micBtn.classList.remove('listening');
    if (waveBox) waveBox.classList.remove('listening');
    statusEl.innerText = "Speech recognized! Review text above and click Analyze.";
  };

  micBtn.addEventListener('click', () => {
    if (listening) {
      analyzerVoiceRec.stop();
    } else {
      const currentLang = localStorage.getItem('medir_lang') || 'en';
      analyzerVoiceRec.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
      analyzerVoiceRec.start();
    }
  });

  submitVoiceBtn.addEventListener('click', () => {
    const text = transcriptEdit.value.trim();
    if (!text) {
      alert("No speech transcript recorded yet. Please tap the microphone and speak.");
      return;
    }
    submitAnalysis({ text: text, title: "Spoken Medical Query", input_type: "voice" });
  });
}

// 6. Tab E: Video Upload
function setupVideoUpload() {
  const videoInput = document.getElementById('videoInputFile');
  const submitBtn = document.getElementById('btnSubmitVideo');

  if (!submitBtn || !videoInput) return;

  submitBtn.addEventListener('click', () => {
    if (!videoInput.files || videoInput.files.length === 0) {
      alert("Please select a video file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', videoInput.files[0]);
    showLoader(true);

    fetch('/api/analyzer/process', { method: 'POST', body: formData })
      .then(res => res.json())
      .then(data => {
        showLoader(false);
        if (data.success && data.simplification) {
          renderAnalysisResults(data.simplification);
        } else {
          alert("Video analysis failed: " + (data.error || "Unknown issue"));
        }
      })
      .catch(() => {
        showLoader(false);
        alert("Error uploading video file.");
      });
  });
}

function submitAnalysis(payload) {
  showLoader(true);

  fetch('/api/analyzer/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    showLoader(false);
    if (data.success && data.simplification) {
      renderAnalysisResults(data.simplification);
    } else {
      alert("Analysis error: " + (data.error || "Could not complete analysis"));
    }
  })
  .catch(() => {
    showLoader(false);
    alert("Connection error contacting MediR analysis service.");
  });
}

function showLoader(visible) {
  const loader = document.getElementById('analyzerLoader');
  const results = document.getElementById('analysisResultsBox');
  if (loader) loader.style.display = visible ? 'block' : 'none';
  if (visible && results) results.style.display = 'none';
}

function renderAnalysisResults(analysis) {
  const resultsBox = document.getElementById('analysisResultsBox');
  if (!resultsBox) return;
  resultsBox.style.display = 'block';

  // 1. Plain Language Summary
  const summaryEl = document.getElementById('resSummary');
  if (summaryEl) {
    summaryEl.innerText = analysis.summary || "Analysis completed.";
    currentSummaryToSpeak = analysis.summary || "";
  }

  // 2. 5-Column Results Table
  // Test Name | Measured Value | Unit | Reference Range | Simple Explanation
  const tbody = document.getElementById('resultsTableBody');
  if (tbody) {
    const tableData = analysis.results_table || [];
    if (tableData.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="5" class="text-center text-muted py-3">
            No quantitative numerical test markers detected in this document/input. General health advice generated above.
          </td>
        </tr>
      `;
    } else {
      tbody.innerHTML = tableData.map(row => {
        const statusBadge = row.status === 'HIGH' 
          ? '<span class="status-badge status-badge-high">HIGH</span>'
          : row.status === 'LOW'
          ? '<span class="status-badge status-badge-low">LOW</span>'
          : '<span class="status-badge status-badge-normal">NORMAL</span>';

        return `
          <tr>
            <td class="fw-bold text-dark">${row.test_name}</td>
            <td class="fw-bold" style="color: var(--primary-green);">${row.measured_value} ${statusBadge}</td>
            <td class="text-muted small">${row.unit}</td>
            <td class="text-muted small">${row.reference_range}</td>
            <td class="small">${row.simple_explanation}</td>
          </tr>
        `;
      }).join('');
    }
  }

  // 3. Observations List
  const obsList = document.getElementById('resObservationsList');
  if (obsList && analysis.important_observations) {
    obsList.innerHTML = analysis.important_observations.map(obs => `
      <li class="mb-2"><strong>Observation:</strong> ${obs}</li>
    `).join('');
  }

  // 4. Unreadable or missing info
  const unreadableBox = document.getElementById('unreadableNoticeBox');
  const unreadableText = document.getElementById('unreadableNoticeText');
  if (unreadableBox && unreadableText) {
    if (analysis.unreadable_or_missing) {
      unreadableText.innerText = analysis.unreadable_or_missing;
      unreadableBox.style.display = 'block';
    } else {
      unreadableBox.style.display = 'none';
    }
  }

  // 5. Doctor Questions
  const docList = document.getElementById('resDoctorQuestionsList');
  if (docList && analysis.recommended_doctor_questions) {
    docList.innerHTML = analysis.recommended_doctor_questions.map(q => `
      <li class="mb-2 d-flex align-items-start gap-2">
        <i class="bi bi-question-circle-fill text-success mt-1"></i>
        <span>${q}</span>
      </li>
    `).join('');
  }

  // 6. Glossary Terms
  const glossaryBox = document.getElementById('resGlossaryContainer');
  if (glossaryBox && analysis.glossary) {
    glossaryBox.innerHTML = analysis.glossary.map(g => `
      <div class="col-md-6">
        <div class="p-3 border rounded h-100" style="background-color: var(--mint-bg);">
          <div class="fw-bold" style="color: var(--primary-green);">${g.term}</div>
          <div class="small text-muted">${g.simple_explanation}</div>
        </div>
      </div>
    `).join('');
  }

  // Smooth scroll down to results
  resultsBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 7. Audio Playback Controls for Spoken Explanations
function setupAudioControls() {
  const playBtn = document.getElementById('btnAudioPlay');
  const pauseBtn = document.getElementById('btnAudioPause');
  const stopBtn = document.getElementById('btnAudioStop');
  const speedSelect = document.getElementById('audioSpeedSelect');

  if (!playBtn) return;

  playBtn.addEventListener('click', () => {
    if (!('speechSynthesis' in window)) {
      alert("Text-to-Speech is not supported in this browser.");
      return;
    }
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      return;
    }
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(currentSummaryToSpeak || "No summary text available to read.");
    const currentLang = localStorage.getItem('medir_lang') || 'en';
    utterance.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
    if (speedSelect) {
      utterance.rate = parseFloat(speedSelect.value) || 1.0;
    }
    window.speechSynthesis.speak(utterance);
  });

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
        window.speechSynthesis.pause();
      }
    });
  }

  if (stopBtn) {
    stopBtn.addEventListener('click', () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    });
  }
}
