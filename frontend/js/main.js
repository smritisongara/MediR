/**
 * MediR AI - Main Universal Client Script
 * Handles: Multilingual i18n, Theme Toggling, Accessibility, and Voice Assistant
 */

// Multilingual i18n Dictionary for Navigation & Core UI
const I18N_DICTIONARY = {
  en: {
    nav_home: "Home",
    nav_dashboard: "Dashboard",
    nav_upload: "Upload Report",
    nav_explain: "AI Explanation",
    nav_chat: "Medical Chatbot",
    nav_hospitals: "Nearby Hospitals",
    nav_presc: "Prescription",
    nav_history: "My Reports",
    nav_login: "Login / Sign Up",
    disclaimer_text: "⚠️ MediR is an educational medical communication assistant, not a doctor. Always consult your qualified healthcare professional.",
    hero_title: "Understand Your Health, Without Language Barriers.",
    hero_subtitle: "Upload your medical report, understand complicated medical terms, translate information into your regional language, and listen to simple explanations with the power of AI.",
    btn_upload_hero: "Upload Medical Report",
    btn_explore_hero: "Explore AI Assistant",
    how_it_works: "How MediR Works",
    step1_title: "1. Upload Your Report",
    step1_desc: "Upload lab tests, doctor notes, or prescriptions in PDF, PNG, JPG format, or snap a live photo.",
    step2_title: "2. AI Understands Info",
    step2_desc: "Intelligent OCR and medical AI extract parameters, check reference bounds, and flag high/low values.",
    step3_title: "3. Get Simple Explanations",
    step3_desc: "Complex medical jargon is broken down into simple terms with custom questions for your doctor.",
    step4_title: "4. Listen in Your Language",
    step4_desc: "Read or listen in Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, Kannada, or Malayalam.",
    voice_assistant_title: "MediR Voice Assistant",
    voice_listening: "Listening to your voice...",
    voice_placeholder: "Speak a command in English or Hindi (e.g. 'Open dashboard', 'डैशबोर्ड खोलो')...",
    btn_close: "Close"
  },
  hi: {
    nav_home: "होम",
    nav_dashboard: "डैशबोर्ड",
    nav_upload: "रिपोर्ट अपलोड करें",
    nav_explain: "AI व्याख्या",
    nav_chat: "मेडिकल चैटबॉट",
    nav_hospitals: "पास के अस्पताल",
    nav_presc: "प्रिस्क्रिप्शन",
    nav_history: "मेरी रिपोर्ट्स",
    nav_login: "लॉगिन / साइन अप",
    disclaimer_text: "⚠️ मेडीआर (MediR) केवल समझने में सहायता के लिए है, यह डॉक्टर का विकल्प नहीं है। हमेशा योग्य डॉक्टर से परामर्श लें।",
    hero_title: "अपनी सेहत को समझें, बिना किसी भाषा की रुकावट के।",
    hero_subtitle: "अपनी मेडिकल रिपोर्ट अपलोड करें, कठिन शब्दों को आसान भाषा में समझें, अपनी मातृभाषा में अनुवाद करें और AI की मदद से आवाज में सुनें।",
    btn_upload_hero: "मेडिकल रिपोर्ट अपलोड करें",
    btn_explore_hero: "AI असिस्टेंट देखें",
    how_it_works: "MediR कैसे काम करता है?",
    step1_title: "1. अपनी रिपोर्ट अपलोड करें",
    step1_desc: "लैब टेस्ट, पर्ची या प्रिस्क्रिप्शन को PDF, इमेज या लाइव कैमरे से फोटो खींचकर अपलोड करें।",
    step2_title: "2. AI रिपोर्ट समझता है",
    step2_desc: "OCR और AI आपकी रिपोर्ट के मान (values) और सामान्य सीमाओं (ranges) की जांच करते हैं।",
    step3_title: "3. सरल भाषा में समझें",
    step3_desc: "कठिन मेडिकल शब्दों को आसान भाषा और डॉक्टर से पूछने वाले प्रश्नों में बदल दिया जाता है।",
    step4_title: "4. अपनी भाषा में सुनें",
    step4_desc: "हिंदी, मराठी, गुजराती, तमिल, तेलुगु या अन्य भाषाओं में अनुवाद करें और बोलकर सुनें।",
    voice_assistant_title: "MediR वॉइस असिस्टेंट",
    voice_listening: "आपकी आवाज़ सुन रहे हैं...",
    voice_placeholder: "अंग्रेजी या हिंदी में बोलें (जैसे 'डैशबोर्ड खोलो', 'अस्पताल दिखाओ')...",
    btn_close: "बंद करें"
  },
  mr: {
    nav_home: "मुख्यपृष्ठ",
    nav_dashboard: "डॅशबोर्ड",
    nav_upload: "अहवाल अपलोड करा",
    nav_explain: "AI स्पष्टीकरण",
    nav_chat: "वैद्यकीय चॅटबॉट",
    nav_hospitals: "जवळची रुग्णालये",
    nav_presc: "प्रिस्क्रिप्शन",
    nav_history: "माझे अहवाल",
    nav_login: "लॉगिन",
    disclaimer_text: "⚠️ MediR हे केवळ शैक्षणिक मदतीसाठी आहे. नेहमी आपल्या डॉक्टरांचा सल्ला घ्या.",
    hero_title: "आपले आरोग्य समजून घ्या, भाषेच्या अडथळ्यांशिवाय.",
    hero_subtitle: "आपला वैद्यकीय अहवाल अपलोड करा, कठीण शब्द सोप्या भाषेत समजून घ्या आणि AI द्वारे ऐका.",
    btn_upload_hero: "अहवाल अपलोड करा",
    btn_explore_hero: "AI सहाय्यक पहा",
    how_it_works: "MediR कसे कार्य करते?",
    step1_title: "1. अहवाल अपलोड करा",
    step1_desc: "PDF किंवा फोटो स्वरूपात अहवाल अपलोड करा.",
    step2_title: "2. AI विश्लेषण",
    step2_desc: "AI आपोआप तपासणी मूल्यांचे विश्लेषण करते.",
    step3_title: "3. सोपे स्पष्टीकरण",
    step3_desc: "कठीण वैद्यकीय शब्द सोप्या भाषेत समजून घ्या.",
    step4_title: "4. आपल्या भाषेत ऐका",
    step4_desc: "मराठीत अनुवाद करा आणि ऑडिओ ऐका."
  },
  gu: {
    nav_home: "હોમ",
    nav_dashboard: "ડેશબોર્ડ",
    nav_upload: "રિપોર્ટ અપલોડ કરો",
    nav_explain: "AI સમજૂતી",
    nav_chat: "મેડિકલ ચેટબોટ",
    nav_hospitals: "નજીકની હોસ્પિટલો",
    nav_presc: "પ્રિસ્ક્રિપ્શન",
    nav_history: "મારા રિપોર્ટ્સ",
    nav_login: "લૉગિન",
    disclaimer_text: "⚠️ MediR ફક્ત સમજવા માટે સહાયક છે, ડૉક્ટરનો વિકલ્પ નથી.",
    hero_title: "તમારા સ્વાસ્થ્યને સમજો, ભાષાના અંતરાય વગર.",
    hero_subtitle: "મેડિકલ રિપોર્ટ અપલોડ કરો, અઘરા શબ્દો સરળ ભાષામાં સમજો અને AI દ્વારા સાંભળો.",
    btn_upload_hero: "રિપોર્ટ અપલોડ કરો",
    btn_explore_hero: "AI સહાયક જુઓ",
    how_it_works: "MediR કેવી રીતે કાર્ય કરે છે?",
    step1_title: "1. રિપોર્ટ અપલોડ કરો",
    step1_desc: "PDF અથવા ફોટો અપલોડ કરો.",
    step2_title: "2. AI સમજૂતી",
    step2_desc: "AI મૂલ્યોનું વિશ્લેષણ કરે છે.",
    step3_title: "3. સરળ શબ્દો",
    step3_desc: "તમારી ભાષામાં સરળ સમજૂતી મેળવો.",
    step4_title: "4. અવાજમાં સાંભળો",
    step4_desc: "ગુજરાતીમાં સાંભળો અને સમજો."
  },
  ta: {
    nav_home: "முகப்பு",
    nav_dashboard: "டாஷ்போர்டு",
    nav_upload: "அறிக்கை பதிவேற்றுக",
    nav_explain: "AI விளக்கம்",
    nav_chat: "மருத்துவ சேட்பாட்",
    nav_hospitals: "அருகிலுள்ள மருத்துவமனைகள்",
    nav_presc: "மருந்து சீட்டு",
    nav_history: "என் அறிக்கைகள்",
    nav_about: "எங்களை பற்றி",
    nav_login: "உள்நுழைக",
    disclaimer_text: "⚠️ MediR கல்வி உதவிக்காக மட்டுமே. மருத்துவரை அணுகவும்.",
    hero_title: "உங்கள் ஆரோக்கியத்தை எளிய மொழியில் புரிந்து கொள்ளுங்கள்.",
    hero_subtitle: "மருத்துவ அறிக்கையை பதிவேற்றி, எளிய தமிழில் புரிந்து கொண்டு குரல் மூலம் கேளுங்கள்.",
    btn_upload_hero: "அறிக்கையை பதிவேற்றுக",
    btn_explore_hero: "AI உதவியாளரை காண்க",
    how_it_works: "MediR எவ்வாறு செயல்படுகிறது?",
    step1_title: "1. அறிக்கையை பதிவேற்றுக",
    step1_desc: "PDF அல்லது புகைப்படத்தை பதிவேற்றவும்.",
    step2_title: "2. AI ஆய்வு",
    step2_desc: "AI அறிக்கையின் மதிப்புகளை சரிபார்க்கிறது.",
    step3_title: "3. எளிய விளக்கம்",
    step3_desc: "எளிதில் புரியும் மொழியில் விளக்கம் பெறவும்.",
    step4_title: "4. தமிழில் கேளுங்கள்",
    step4_desc: "தமிழில் மொழிபெயர்த்து குரல் மூலம் கேளுங்கள்."
  },
  te: {
    nav_home: "హోమ్",
    nav_dashboard: "డ్యాష్‌బోర్డ్",
    nav_upload: "నివేదిక అప్‌లోడ్ చేయండి",
    nav_explain: "AI వివరణ",
    nav_chat: "మెడికల్ చాట్‌బాట్",
    nav_hospitals: "సమీప ఆసుపత్రులు",
    nav_presc: "ప్రిస్క్రిప్షన్",
    nav_history: "నా నివేదికలు",
    nav_about: "మా గురించి",
    nav_login: "లాగిన్",
    disclaimer_text: "⚠️ MediR కేవలం అర్థం చేసుకోవడానికి మాత్రమే. వైద్యుడిని సంప్రదించండి.",
    hero_title: "మీ ఆరోగ్యాన్ని సులభమైన తెలుగులో అర్థం చేసుకోండి.",
    hero_subtitle: "వైద్య నివేదికను అప్‌లోడ్ చేసి, కఠిన పదాలను సులభంగా అర్థం చేసుకోండి.",
    btn_upload_hero: "నివేదిక అప్‌లోడ్ చేయండి",
    btn_explore_hero: "AI అసిస్టెంట్ చూడండి",
    how_it_works: "MediR ఎలా పనిచేస్తుంది?",
    step1_title: "1. నివేదిక అప్‌లోడ్",
    step1_desc: "PDF లేదా ఫోటో అప్‌లోడ్ చేయండి.",
    step2_title: "2. AI విశ్లేషణ",
    step2_desc: "AI ఆరోగ్య విలువల శ్రేణులను తనిఖీ చేస్తుంది.",
    step3_title: "3. సరళమైన వివరణ",
    step3_desc: "సులభమైన భాషలో నివేదిక అర్థం చేసుకోండి.",
    step4_title: "4. తెలుగులో వినండి",
    step4_desc: "మీ మాతృభాషలో ఆడియో వినండి."
  },
  bn: {
    nav_home: "হোম",
    nav_dashboard: "ড্যাশবোর্ড",
    nav_upload: "রিপোর্ট আপলোড",
    nav_explain: "AI ব্যাখ্যা",
    nav_chat: "মেডিকেল চ্যাটবট",
    nav_hospitals: "কাছের হাসপাতাল",
    nav_presc: "প্রেসক্রিপশন",
    nav_history: "আমার রিপোর্ট",
    nav_about: "আমাদের সম্পর্কে",
    nav_login: "লগইন",
    disclaimer_text: "⚠️ MediR কেবল শিক্ষামূলক সহায়ক, ডাক্তারের বিকল্প নয়।",
    hero_title: "ভাষার বাধা ছাড়াই নিজের স্বাস্থ্য বুঝুন।",
    hero_subtitle: "মেডিকেল রিপোর্ট আপলোড করুন, সহজে বুঝুন এবং বাংলায় শুনুন।",
    btn_upload_hero: "রিপোর্ট আপলোড করুন",
    btn_explore_hero: "AI সহকারী দেখুন",
    how_it_works: "MediR কীভাবে কাজ করে?",
    step1_title: "1. রিপোর্ট আপলোড",
    step1_desc: "PDF বা ছবি আপলোড করুন।",
    step2_title: "2. AI বিশ্লেষণ",
    step2_desc: "AI স্বাস্থ্যের মান যাচাই করে।",
    step3_title: "3. সহজ ব্যাখ্যা",
    step3_desc: "কঠিন শব্দ সহজ বাংলায় বুঝুন।",
    step4_title: "4. বাংলায় শুনুন",
    step4_desc: "ভয়েস অ্যাসিস্ট্যান্টের মাধ্যমে শুনুন।"
  }
};

// ----------------- Theme Switcher (Light / Dark) -----------------
function initTheme() {
  const savedTheme = localStorage.getItem('medir_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const newTheme = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('medir_theme', newTheme);
  updateThemeIcon(newTheme);
  
  // Inform backend session
  fetch('/api/auth/preferences', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ theme: newTheme })
  }).catch(() => {});
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeToggleIcon');
  if (icon) {
    if (theme === 'dark') {
      icon.className = 'bi bi-sun-fill text-warning';
    } else {
      icon.className = 'bi bi-moon-stars-fill text-primary';
    }
  }
}

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
}

function toggleContrast() {
  const current = document.documentElement.getAttribute('data-contrast');
  if (current === 'high') {
    document.documentElement.removeAttribute('data-contrast');
  } else {
    document.documentElement.setAttribute('data-contrast', 'high');
  }
}

// ----------------- Voice Assistant Controller -----------------
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
  recognition.interimResults = false;
  
  // Set language from preference
  const currentLang = localStorage.getItem('medir_lang') || 'en';
  recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
  
  recognition.onstart = () => {
    isListening = true;
    updateVoiceUI(true, "Listening to your voice...");
  };
  
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('voiceTranscriptText').innerText = `"${transcript}"`;
    processSpokenCommand(transcript);
  };
  
  recognition.onerror = (event) => {
    isListening = false;
    updateVoiceUI(false, `Error: ${event.error}. Please try again.`);
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
    alert("Voice recognition is not supported in this browser. Please use Chrome, Edge, or Safari.");
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
  updateVoiceUI(false, "Processing your voice command...");
  
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
      document.getElementById('voiceReplyText').innerText = cmd.speech_reply;
      
      // Execute the action safely
      setTimeout(() => {
        executeVoiceAction(cmd);
      }, 1200);
    } else {
      const reply = data.response || "I could not identify that action. Please check the voice command list.";
      speakText(reply);
      document.getElementById('voiceReplyText').innerText = reply;
    }
  })
  .catch(err => {
    document.getElementById('voiceReplyText').innerText = "Command processing failed. Please try again.";
  });
}

function executeVoiceAction(cmd) {
  if (cmd.action === 'NAVIGATE' && cmd.target) {
    window.location.href = cmd.target;
  } else if (cmd.action === 'THEME' && cmd.target) {
    document.documentElement.setAttribute('data-theme', cmd.target);
    localStorage.setItem('medir_theme', cmd.target);
    updateThemeIcon(cmd.target);
  } else if (cmd.action === 'LANGUAGE' && cmd.target) {
    setLanguage(cmd.target);
  } else if (cmd.action === 'STOP_SPEAK') {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  } else if (cmd.action === 'CAMERA') {
    window.location.href = 'upload.html#camera';
  }
}

function speakText(text, lang = null) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  
  const utterance = new SpeechSynthesisUtterance(text);
  const preferredLang = lang || localStorage.getItem('medir_lang') || 'en';
  utterance.lang = preferredLang === 'hi' ? 'hi-IN' : 'en-US';
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}

// ----------------- DOM Initialization -----------------
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initLanguage();
  initVoiceAssistant();
});
