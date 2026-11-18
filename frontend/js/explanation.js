/**
 * MediR AI - Report Explanation & Audio Playback Controller
 */

let currentExplanationText = "";
let currentSpeechUtterance = null;
let isAudioPaused = false;
let currentReportId = null;

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const reportId = urlParams.get('id');
  currentReportId = reportId;

  if (reportId) {
    loadReportDetails(reportId);
  } else {
    // Check sessionStorage
    const cached = sessionStorage.getItem('current_report');
    if (cached) {
      const data = JSON.parse(cached);
      renderReportExplanation(data);
    } else {
      // Default to demo sample if nothing uploaded yet
      loadDefaultDemo();
    }
  }

  setupAudioControls();
  setupLanguageSwitcher();
});

function loadReportDetails(id) {
  fetch(`/api/reports/${id}`)
    .then(res => res.json())
    .then(data => {
      if (data.success && data.report) {
        const r = data.report;
        renderReportExplanation({
          report_id: r.report_id,
          original_filename: r.original_filename,
          extracted_text: r.extracted_text,
          simplification: {
            summary: r.simplified_explanation,
            key_findings: r.key_findings,
            abnormal_values: r.abnormal_values,
            glossary: [],
            recommended_doctor_questions: [
              "What do these numbers mean for my daily health?",
              "Do I need any dietary modifications?",
              "When should I repeat this test?"
            ]
          }
        });
      }
    })
    .catch(() => loadDefaultDemo());
}

function loadDefaultDemo() {
  fetch('/sample_data/sample_cbc_report.txt')
    .then(res => res.text())
    .then(text => {
      fetch('/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      })
      .then(res => res.json())
      .then(data => {
        renderReportExplanation({
          original_filename: "Sample CBC Blood Test.txt",
          extracted_text: text,
          simplification: data.simplification
        });
      });
    });
}

function renderReportExplanation(data) {
  const simp = data.simplification || {};
  
  // Set report titles
  const titleEl = document.getElementById('reportTitle');
  if (titleEl) titleEl.innerText = data.original_filename || "Medical Report";

  // Summary
  const summaryEl = document.getElementById('explanationSummary');
  if (summaryEl) summaryEl.innerText = simp.summary || "Explanation generated.";
  currentExplanationText = simp.summary || "";

  // Abnormal Values Badges & Cards
  const abnormalContainer = document.getElementById('abnormalValuesList');
  if (abnormalContainer) {
    const abnormals = simp.abnormal_values || [];
    if (abnormals.length === 0) {
      abnormalContainer.innerHTML = `
        <div class="alert alert-success d-flex align-items-center gap-2">
          <i class="bi bi-check-circle-fill fs-5"></i>
          <div>All identified laboratory values appear to be within normal reference bounds.</div>
        </div>
      `;
    } else {
      abnormalContainer.innerHTML = abnormals.map(a => `
        <div class="col-md-6 mb-3">
          <div class="p-3 border rounded-3 h-100" style="background-color: var(--bg-card-subtle);">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="fw-bold">${a.parameter}</span>
              <span class="status-badge status-badge-${a.status.toLowerCase()}">${a.status}</span>
            </div>
            <div class="fs-5 fw-bold text-primary mb-1">${a.value}</div>
            <div class="small text-muted mb-2">Standard Range: ${a.reference_range}</div>
            <p class="small mb-0 text-secondary">${a.patient_note || a.meaning}</p>
          </div>
        </div>
      `).join('');
    }
  }

  // Key Findings Table
  const findingsTable = document.getElementById('keyFindingsTableBody');
  if (findingsTable) {
    const findings = simp.key_findings || [];
    findingsTable.innerHTML = findings.map(f => `
      <tr>
        <td class="fw-semibold">${f.parameter}</td>
        <td><span class="fw-bold">${f.value}</span></td>
        <td class="text-muted">${f.reference_range}</td>
        <td><span class="status-badge status-badge-${f.status.toLowerCase()}">${f.status}</span></td>
        <td class="small">${f.meaning}</td>
      </tr>
    `).join('');
  }

  // Doctor Questions
  const questionsList = document.getElementById('doctorQuestionsList');
  if (questionsList) {
    const qList = simp.recommended_doctor_questions || [];
    questionsList.innerHTML = qList.map(q => `
      <li class="mb-2 d-flex align-items-start gap-2">
        <i class="bi bi-question-circle-fill text-primary mt-1"></i>
        <span>${q}</span>
      </li>
    `).join('');
  }

  // Original Extracted Text
  const origTextEl = document.getElementById('originalExtractedText');
  if (origTextEl) {
    origTextEl.innerText = data.extracted_text || "No text available.";
  }

  // Medical Glossary matches
  const glossaryBox = document.getElementById('glossaryTermsBox');
  if (glossaryBox && simp.glossary) {
    glossaryBox.innerHTML = simp.glossary.map(g => `
      <div class="col-md-6 mb-2">
        <div class="p-2 border rounded-2 bg-light">
          <strong>${g.term}:</strong> <span class="text-muted small">${g.simple_explanation}</span>
        </div>
      </div>
    `).join('');
  }

  // Setup Chatbot link
  const askChatBtn = document.getElementById('btnAskChatbotWithContext');
  if (askChatBtn && data.report_id) {
    askChatBtn.href = `chatbot.html?report_id=${data.report_id}`;
  }
}

// ----------------- Audio Playback Controller -----------------
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

    if (isAudioPaused) {
      window.speechSynthesis.resume();
      isAudioPaused = false;
      playBtn.classList.add('active');
      return;
    }

    window.speechSynthesis.cancel();
    
    const textToSpeak = currentExplanationText || "No text available to read.";
    currentSpeechUtterance = new SpeechSynthesisUtterance(textToSpeak);
    
    const targetLang = document.getElementById('explanationLangSelect')?.value || 'en';
    currentSpeechUtterance.lang = targetLang === 'hi' ? 'hi-IN' : 'en-US';
    
    if (speedSelect) {
      currentSpeechUtterance.rate = parseFloat(speedSelect.value) || 1.0;
    }

    currentSpeechUtterance.onend = () => {
      playBtn.classList.remove('active');
      isAudioPaused = false;
    };

    window.speechSynthesis.speak(currentSpeechUtterance);
    playBtn.classList.add('active');
  });

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
        window.speechSynthesis.pause();
        isAudioPaused = true;
        playBtn.classList.remove('active');
      }
    });
  }

  if (stopBtn) {
    stopBtn.addEventListener('click', () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        isAudioPaused = false;
        playBtn.classList.remove('active');
      }
    });
  }
}

// ----------------- Live Explanation Translation -----------------
function setupLanguageSwitcher() {
  const langSelect = document.getElementById('explanationLangSelect');
  if (!langSelect) return;

  langSelect.addEventListener('change', () => {
    const targetLang = langSelect.value;
    const textToTranslate = currentExplanationText;

    if (!textToTranslate) return;

    fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: textToTranslate, target_lang: targetLang })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById('explanationSummary').innerText = data.translated_text;
        currentExplanationText = data.translated_text;
      }
    });
  });
}
