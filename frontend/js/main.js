/**
 * MediR AI - Main Universal Client Script
 * Handles: Multilingual i18n, Theme Toggling, Accessibility, and Advanced Voice Assistant
 */

// Multilingual i18n Dictionary for Navigation & Core UI
const I18N_DICTIONARY = {
  en: {
    nav_home: "Home",
    nav_dashboard: "Dashboard",
    nav_analyzer: "AI Analyzer",
    nav_upload: "Upload",
    nav_chat: "Medical Chatbot",
    nav_hospitals: "Nearby Hospitals",
    nav_presc: "Prescription",
    nav_history: "My Reports",
    nav_profile: "Profile & Settings",
    nav_login: "Login / Sign Up",
    disclaimer_text: "⚠️ MediR is an educational medical communication assistant, not a doctor. Always consult your qualified healthcare professional.",
    hero_title: "Understand Your Health, Without Language Barriers.",
    hero_subtitle: "Upload your medical report, understand complicated medical terms, translate information into your regional language, and listen to simple explanations with the power of AI.",
    btn_upload_hero: "Analyze Medical Report",
    btn_explore_hero: "Explore AI Assistant",
    how_it_works: "How MediR Works",
    step1_title: "1. Submit Medical Info",
    step1_desc: "Type symptoms, upload lab PDFs, snap camera photos, speak via voice, or upload video advice.",
    step2_title: "2. Advanced AI Analysis",
    step2_desc: "AI extracts lab values, cross-references clinical biological bounds, and flags high/low parameters.",
    step3_title: "3. 5-Column Results Table",
    step3_desc: "View Test Name, Value, Unit, Reference Range, and Simple Plain-Language Explanations.",
    step4_title: "4. Multilingual & Spoken Voice",
    step4_desc: "Translate into 10 regional Indian languages or listen aloud through natural speech synthesis.",
    voice_assistant_title: "MediR Advanced Voice AI",
    voice_listening: "Listening... (Speak in English or Hindi)",
    voice_placeholder: "Say: 'Open dashboard', 'Upload report', 'Find nearby hospitals', or ask any medical question...",
    btn_close: "Close"
  },
  hi: {
    nav_home: "होम",
    nav_dashboard: "डैशबोर्ड",
    nav_analyzer: "AI विश्लेषक",
    nav_upload: "अपलोड",
    nav_chat: "मेडिकल चैटबॉट",
    nav_hospitals: "पास के अस्पताल",
    nav_presc: "प्रिस्क्रिप्शन",
    nav_history: "मेरी रिपोर्ट्स",
    nav_profile: "प्रोफ़ाइल व सेटिंग्स",
    nav_login: "लॉगिन / साइन अप",
    disclaimer_text: "⚠️ मेडीआर (MediR) केवल समझने में सहायता के लिए है, यह डॉक्टर का विकल्प नहीं है। हमेशा योग्य डॉक्टर से परामर्श लें।",
    hero_title: "अपनी सेहत को समझें, बिना किसी भाषा की रुकावट के।",
    hero_subtitle: "अपनी मेडिकल रिपोर्ट अपलोड करें, कठिन शब्दों को आसान भाषा में समझें, अपनी मातृभाषा में अनुवाद करें और AI की मदद से आवाज में सुनें।",
    btn_upload_hero: "मेडिकल रिपोर्ट जांचें",
    btn_explore_hero: "AI असिस्टेंट देखें",
    how_it_works: "MediR कैसे काम करता है?",
    step1_title: "1. जानकारी सबमिट करें",
    step1_desc: "लक्षण लिखें, PDF रिपोर्ट अपलोड करें, फोटो खींचें, आवाज से बोलें या वीडियो अपलोड करें।",
    step2_title: "2. उन्नत AI विश्लेषण",
    step2_desc: "AI रिपोर्ट के मान और सामान्य सीमाओं की स्वचालित जांच करता है।",
    step3_title: "3. 5-कॉलम परिणाम तालिका",
    step3_desc: "टेस्ट नाम, मान, यूनिट, सामान्य सीमा और सरल व्याख्या देखें।",
    step4_title: "4. मातृभाषा में सुनें",
    step4_desc: "हिंदी, मराठी, गुजराती, तमिल आदि में अनुवाद करें और बोलकर सुनें।",
    voice_assistant_title: "MediR उन्नत वॉइस AI",
    voice_listening: "आपकी आवाज़ सुन रहे हैं...",
    voice_placeholder: "बोलें: 'डैशबोर्ड खोलो', 'अस्पताल दिखाओ', 'डार्क मोड चालू करो'...",
    btn_close: "बंद करें"
  }
};

// ----------------- Multilingual Language Switcher -----------------
function initLanguage() {
  const savedLang = localStorage.getItem('medir_lang') || 'en';
  setLanguage(savedLang, false);
}

function setLanguage(lang, syncServer = true) {
  localStorage.setItem('medir_lang', lang);
  const langSelector = document.getElementById('globalLanguageSelect');
  if (langSelector) langSelector.value = lang;
  
  const translations = I18N_DICTIONARY[lang] || I18N_DICTIONARY['en'];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (translations[key]) {
      el.textContent = translations[key];
    }
  });

  if (syncServer) {
    fetch('/api/auth/preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language: lang })
    }).catch(() => {});
  }
}

// ----------------- Accessibility Helpers -----------------
let currentFontSize = 16;
function adjustFontSize(delta) {
  currentFontSize = Math.max(13, Math.min(22, currentFontSize + delta));
  document.documentElement.style.setProperty('--base-font-size', `${currentFontSize}px`);
  document.body.style.fontSize = `${currentFontSize}px`;
}

function toggleContrast() {
  const current = document.documentElement.getAttribute('data-contrast');
  if (current === 'high') {
    document.documentElement.removeAttribute('data-contrast');
  } else {
    document.documentElement.setAttribute('data-contrast', 'high');
  }
}

// ----------------- Advanced Voice Assistant Controller -----------------
let recognition = null;
let isListening = false;

function initVoiceAssistant() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.warn("Speech Recognition API not supported in this browser.");
    return;
  }
  
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true; // Show live interim words as the user speaks!
  
  const currentLang = localStorage.getItem('medir_lang') || 'en';
  recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
  
  recognition.onstart = () => {
    isListening = true;
    updateVoiceUI(true, "Listening... (Speak clearly into your microphone)");
  };
  
  recognition.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        finalTranscript += event.results[i][0].transcript;
      } else {
        interimTranscript += event.results[i][0].transcript;
      }
    }

    const displayText = finalTranscript || interimTranscript;
    const transcriptEl = document.getElementById('voiceTranscriptText');
    if (transcriptEl) transcriptEl.innerText = `"${displayText}"`;

    if (finalTranscript) {
      processSpokenCommand(finalTranscript);
    }
  };
  
  recognition.onerror = (event) => {
    isListening = false;
    updateVoiceUI(false, `Voice recognition notice: ${event.error}. Click to retry.`);
  };
  
  recognition.onend = () => {
    isListening = false;
    const btn = document.getElementById('floatingVoiceBtn');
    if (btn) btn.classList.remove('listening');
  };
}

function toggleVoiceModal() {
  const modal = document.getElementById('voiceModal');
  if (!modal) return;
  
  if (modal.style.display === 'flex') {
    modal.style.display = 'none';
    if (recognition && isListening) recognition.stop();
  } else {
    modal.style.display = 'flex';
    startVoiceListening();
  }
}

function startVoiceListening() {
  if (!recognition) {
    initVoiceAssistant();
  }
  if (recognition) {
    try {
      const currentLang = localStorage.getItem('medir_lang') || 'en';
      recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
      recognition.start();
    } catch (e) {
      console.warn("Recognition already active", e);
    }
  } else {
    alert("Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.");
  }
}

function updateVoiceUI(listening, statusText) {
  const statusEl = document.getElementById('voiceStatusText');
  const waveEl = document.getElementById('soundWaveBox');
  const btn = document.getElementById('floatingVoiceBtn');
  
  if (statusEl) statusEl.innerText = statusText;
  if (waveEl) {
    if (listening) waveEl.classList.add('listening');
    else waveEl.classList.remove('listening');
  }
  if (btn) {
    if (listening) btn.classList.add('listening');
    else btn.classList.remove('listening');
  }
}

function processSpokenCommand(transcript) {
  updateVoiceUI(false, "Processing your request with MediR AI...");
  
  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: transcript, is_voice: true })
  })
  .then(res => res.json())
  .then(data => {
    if (data.is_command && data.command) {
      const cmd = data.command;
      speakText(cmd.speech_reply);
      const replyEl = document.getElementById('voiceReplyText');
      if (replyEl) replyEl.innerText = cmd.speech_reply;
      
      // Execute the navigation or UI action safely
      setTimeout(() => {
        executeVoiceAction(cmd);
      }, 1200);
    } else {
      // General Medical AI Response spoken back!
      const reply = data.response || "Here is what I found.";
      const replyEl = document.getElementById('voiceReplyText');
      if (replyEl) replyEl.innerText = reply;
      speakText(reply);
    }
  })
  .catch(() => {
    const replyEl = document.getElementById('voiceReplyText');
    if (replyEl) replyEl.innerText = "Network issue processing command. Please try again.";
  });
}

function executeVoiceAction(cmd) {
  if (cmd.action === 'NAVIGATE' && cmd.target) {
    window.location.href = cmd.target;
  } else if (cmd.action === 'THEME' && cmd.target) {
    if (typeof applyTheme === 'function') {
      applyTheme(cmd.target);
    } else {
      document.documentElement.setAttribute('data-theme', cmd.target);
      localStorage.setItem('medir_theme', cmd.target);
    }
  } else if (cmd.action === 'LANGUAGE' && cmd.target) {
    setLanguage(cmd.target);
  } else if (cmd.action === 'STOP_SPEAK') {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  } else if (cmd.action === 'CAMERA') {
    window.location.href = 'analyzer.html#photo';
  }
}

function speakText(text, lang = null) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  
  // Strip markdown characters before speaking for natural speech
  const cleanSpoken = text.replace(/[*#_`~>]/g, '').replace(/⚠️/g, 'Warning: ');
  const utterance = new SpeechSynthesisUtterance(cleanSpoken);
  const preferredLang = lang || localStorage.getItem('medir_lang') || 'en';
  utterance.lang = preferredLang === 'hi' ? 'hi-IN' : 'en-US';
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}

// ----------------- DOM Initialization -----------------
document.addEventListener('DOMContentLoaded', () => {
  initLanguage();
  initVoiceAssistant();
});
