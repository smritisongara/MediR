import re
import difflib

# Locales for browser Web Speech API
VOICE_LOCALES = {
    "en": "en-US",
    "hi": "hi-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "bn": "bn-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "pa": "pa-IN",
    "kn": "kn-IN",
    "ml": "ml-IN"
}

# Advanced Intent Definitions with Expanded Colloquial Patterns (English & Hindi)
INTENTS = [
    {
        "id": "NAVIGATE_DASHBOARD",
        "action": "NAVIGATE",
        "target": "dashboard.html",
        "speech_reply": "Opening your patient dashboard.",
        "keywords": [
            "dashboard", "open dashboard", "go to dashboard", "show dashboard", "take me to dashboard",
            "home dashboard", "main dashboard", "view dashboard",
            "डैशबोर्ड", "डैशबोर्ड खोलो", "डैशबोर्ड दिखाओ", "डैशबोर्ड पर जाओ", "डैशबोर्ड खोलिए", "मुख्य पृष्ठ"
        ],
        "regex": r"\b(dashboard|डैशबोर्ड)\b"
    },
    {
        "id": "NAVIGATE_ANALYZER",
        "action": "NAVIGATE",
        "target": "analyzer.html",
        "speech_reply": "Opening AI Medical Problem and Report Analyzer.",
        "keywords": [
            "analyzer", "open analyzer", "analyze report", "medical analyzer", "symptom analyzer",
            "report analyzer", "check my report", "analyze my symptoms",
            "एनालाइजर", "रिपोर्ट जांचो", "रिपोर्ट एनालाइज करो", "जांच करो", "लक्षण बताओ"
        ],
        "regex": r"\b(analyz|analyse|analyzer|एनालाइजर|जांच)\b"
    },
    {
        "id": "NAVIGATE_UPLOAD",
        "action": "NAVIGATE",
        "target": "upload.html",
        "speech_reply": "Opening medical report upload page.",
        "keywords": [
            "upload", "upload report", "upload medical report", "upload file", "open upload",
            "upload document", "submit report", "upload my report", "upload test",
            "अपलोड", "अपलोड करो", "रिपोर्ट अपलोड करो", "फाइल अपलोड", "दस्तावेज अपलोड", "मेडिकल रिपोर्ट अपलोड"
        ],
        "regex": r"\b(upload|अपलोड)\b"
    },
    {
        "id": "NAVIGATE_HOSPITALS",
        "action": "NAVIGATE",
        "target": "hospital.html",
        "speech_reply": "Searching for nearby verified hospitals on the interactive map.",
        "keywords": [
            "hospital", "hospitals", "find hospital", "nearby hospitals", "find nearby hospitals",
            "show hospitals", "emergency hospital", "locate hospital", "nearest hospital", "clinic",
            "अस्पताल", "हॉस्पिटल", "अस्पताल दिखाओ", "मेरे पास के अस्पताल", "पास का अस्पताल", "दवाखाना", "इमरजेंसी अस्पताल"
        ],
        "regex": r"\b(hospital|hospitals|clinic|emergency|अस्पताल|हॉस्पिटल)\b"
    },
    {
        "id": "NAVIGATE_CHATBOT",
        "action": "NAVIGATE",
        "target": "chatbot.html",
        "speech_reply": "Opening MediR Medical AI Chatbot.",
        "keywords": [
            "chatbot", "open chatbot", "medical chatbot", "ask ai", "talk to ai", "chat with ai",
            "open assistant", "medical assistant", "start chat",
            "चैटबॉट", "चैटबॉट खोलो", "एआई से बात करो", "मददगार खोलो", "चैट करो"
        ],
        "regex": r"\b(chatbot|chat|assistant|चैटबॉट|चैट)\b"
    },
    {
        "id": "NAVIGATE_PRESCRIPTION",
        "action": "NAVIGATE",
        "target": "prescription.html",
        "speech_reply": "Opening prescription scanner and dosage guide.",
        "keywords": [
            "prescription", "open prescription", "scan prescription", "medicine prescription",
            "dosage guide", "doctor prescription", "read prescription",
            "प्रिस्क्रिप्शन", "पर्चा", "दवा का पर्चा", "प्रिस्क्रिप्शन स्कैन करो", "पर्चा दिखाओ", "दवाई बताओ"
        ],
        "regex": r"\b(prescription|rx|medicine|dosage|प्रिस्क्रिप्शन|पर्चा)\b"
    },
    {
        "id": "NAVIGATE_HISTORY",
        "action": "NAVIGATE",
        "target": "history.html",
        "speech_reply": "Opening your saved medical reports history.",
        "keywords": [
            "history", "my reports", "saved reports", "previous reports", "view history",
            "past reports", "report history",
            "हिस्ट्री", "मेरी रिपोर्ट्स", "पुराने रिपोर्ट", "पिछली रिपोर्ट", "इतिहास दिखाओ"
        ],
        "regex": r"\b(history|previous reports|saved reports|हिस्ट्री|पिछली रिपोर्ट)\b"
    },
    {
        "id": "ACTION_DARK_MODE",
        "action": "THEME",
        "target": "dark",
        "speech_reply": "Switching to dark mode theme.",
        "keywords": [
            "dark mode", "switch to dark mode", "enable dark mode", "turn on dark mode",
            "night mode", "dark theme",
            "डार्क मोड", "डार्क मोड चालू करो", "डार्क थीम", "नाइट मोड", "रात का मोड"
        ],
        "regex": r"\b(dark mode|night mode|डार्क मोड|नाइट मोड)\b"
    },
    {
        "id": "ACTION_LIGHT_MODE",
        "action": "THEME",
        "target": "light",
        "speech_reply": "Switching to light mode theme.",
        "keywords": [
            "light mode", "switch to light mode", "enable light mode", "turn on light mode",
            "day mode", "light theme",
            "लाइट मोड", "लाइट मोड चालू करो", "लाइट थीम", "डे मोड", "दिन का मोड"
        ],
        "regex": r"\b(light mode|day mode|लाइट मोड|डे मोड)\b"
    },
    {
        "id": "ACTION_LANGUAGE_HI",
        "action": "LANGUAGE",
        "target": "hi",
        "speech_reply": "भाषा बदलकर हिंदी कर दी गई है।",
        "keywords": [
            "hindi", "translate into hindi", "change language to hindi", "switch to hindi", "hindi language",
            "हिंदी", "हिंदी में अनुवाद करो", "भाषा हिंदी करो", "हिंदी करो"
        ],
        "regex": r"\b(hindi|हिन्दी|हिंदी)\b"
    },
    {
        "id": "ACTION_LANGUAGE_EN",
        "action": "LANGUAGE",
        "target": "en",
        "speech_reply": "Language switched to English.",
        "keywords": [
            "english", "switch to english", "change language to english", "english language",
            "अंग्रेजी", "अंग्रेजी करो", "इंग्लिश करो"
        ],
        "regex": r"\b(english|अंग्रेजी|इंग्लिश)\b"
    },
    {
        "id": "ACTION_SPEAK_REPORT",
        "action": "SPEAK_REPORT",
        "target": None,
        "speech_reply": "Reading your simplified medical report aloud.",
        "keywords": [
            "read aloud", "read my report", "read report aloud", "speak report", "read it to me", "read out",
            "पढ़कर सुनाओ", "मेरी रिपोर्ट पढ़कर सुनाओ", "सुनाओ", "जोर से पढ़ो"
        ],
        "regex": r"\b(read aloud|speak report|पढ़कर सुनाओ|सुनाओ)\b"
    },
    {
        "id": "ACTION_STOP_SPEAK",
        "action": "STOP_SPEAK",
        "target": None,
        "speech_reply": "Stopping audio playback.",
        "keywords": [
            "stop speaking", "stop reading", "be quiet", "stop audio", "stop voice", "shut up", "silence",
            "बोलना बंद करो", "बंद करो", "चुप हो जाओ", "रुको", "आवाज बंद करो"
        ],
        "regex": r"\b(stop|quiet|silence|बंद करो|रुको|चुप)\b"
    },
    {
        "id": "ACTION_CAMERA",
        "action": "CAMERA",
        "target": None,
        "speech_reply": "Opening camera viewfinder to snap your medical document.",
        "keywords": [
            "camera", "take photo", "take a photo", "open camera", "capture photo", "snap photo", "photograph",
            "फोटो खींचो", "कैमरा खोलो", "कैमरा चालू करो", "तस्वीर खींचो"
        ],
        "regex": r"\b(camera|photo|snapshot|कैमरा|फोटो|तस्वीर)\b"
    },
    {
        "id": "ACTION_HELP",
        "action": "HELP",
        "target": None,
        "speech_reply": "You can say: Open dashboard, Upload report, Analyze symptoms, Find nearby hospitals, Switch to dark mode, or ask any medical question.",
        "keywords": [
            "help", "help me", "what can you do", "voice commands", "show commands", "instructions",
            "मदद", "मदद करो", "सहायता", "कमांड बताओ"
        ],
        "regex": r"\b(help|commands|instructions|मदद|सहायता)\b"
    }
]

def parse_voice_command(spoken_text):
    """
    Advanced Natural Language Understanding (NLU) Engine.
    Combines:
    1. Exact keyword & multi-word phrase matching
    2. Regular expression pattern extraction
    3. Fuzzy string matching for misheard or accented speech
    4. Seamless fall-through to Clinical Medical Q&A if text is a medical inquiry
    """
    clean_text = spoken_text.strip().lower()
    # Strip terminal punctuation (periods, commas, question marks, exclamation marks)
    clean_text = re.sub(r'[.,?!;:।]+$', '', clean_text).strip()

    # 1. Exact or Substring match
    for intent in INTENTS:
        for kw in intent["keywords"]:
            if kw == clean_text or f" {kw} " in f" {clean_text} ":
                return {
                    "matched": True,
                    "action": intent["action"],
                    "target": intent["target"],
                    "speech_reply": intent["speech_reply"],
                    "transcript": spoken_text,
                    "confidence": 0.98,
                    "intent_id": intent["id"]
                }

    # 2. Regular Expression match
    for intent in INTENTS:
        if re.search(intent["regex"], clean_text, re.IGNORECASE):
            return {
                "matched": True,
                "action": intent["action"],
                "target": intent["target"],
                "speech_reply": intent["speech_reply"],
                "transcript": spoken_text,
                "confidence": 0.90,
                "intent_id": intent["id"]
            }

    # 3. Fuzzy string similarity match (threshold > 0.75)
    best_match = None
    highest_score = 0.0

    for intent in INTENTS:
        for kw in intent["keywords"]:
            ratio = difflib.SequenceMatcher(None, clean_text, kw).ratio()
            if ratio > highest_score:
                highest_score = ratio
                best_match = intent

    if highest_score >= 0.72 and best_match:
        return {
            "matched": True,
            "action": best_match["action"],
            "target": best_match["target"],
            "speech_reply": best_match["speech_reply"],
            "transcript": spoken_text,
            "confidence": round(highest_score, 2),
            "intent_id": best_match["id"]
        }

    # 4. If not a navigation/action command, it is an Advanced Medical Question!
    return {
        "matched": False,
        "action": "MEDICAL_AI_QUERY",
        "target": None,
        "speech_reply": None,  # Will be answered by Advanced Medical AI
        "transcript": spoken_text,
        "confidence": 0.60,
        "intent_id": "AI_MEDICAL_QUERY"
    }

COMMAND_MAPPINGS = INTENTS
