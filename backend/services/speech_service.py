import re

# Voice language locale tags for browser Web Speech API
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

# Predefined voice commands for both English and Hindi
COMMAND_MAPPINGS = [
    # Dashboard
    {
        "action": "NAVIGATE",
        "target": "dashboard.html",
        "speech_reply": "Opening your patient dashboard.",
        "patterns": ["open dashboard", "go to dashboard", "dashboard", "डैशबोर्ड खोलो", "डैशबोर्ड"]
    },
    # Upload Report
    {
        "action": "NAVIGATE",
        "target": "upload.html",
        "speech_reply": "Opening medical report upload page.",
        "patterns": ["upload medical report", "upload report", "open upload", "मेडिकल रिपोर्ट अपलोड करो", "रिपोर्ट अपलोड करो"]
    },
    # Explain Report
    {
        "action": "NAVIGATE",
        "target": "explanation.html",
        "speech_reply": "Navigating to AI report explanation.",
        "patterns": ["explain my report", "explain report", "show explanation", "मेरी रिपोर्ट समझाओ", "रिपोर्ट समझाओ"]
    },
    # Chatbot
    {
        "action": "NAVIGATE",
        "target": "chatbot.html",
        "speech_reply": "Opening AI medical chatbot.",
        "patterns": ["open medical chatbot", "open chatbot", "ask ai", "चैटबॉट खोलो", "मददगार खोलो"]
    },
    # Hospitals
    {
        "action": "NAVIGATE",
        "target": "hospitals.html",
        "speech_reply": "Searching for nearby hospitals on the interactive map.",
        "patterns": ["find nearby hospitals", "nearby hospitals", "find hospital", "मेरे पास के अस्पताल दिखाओ", "अस्पताल दिखाओ", "अस्पताल"]
    },
    # Prescription
    {
        "action": "NAVIGATE",
        "target": "prescription.html",
        "speech_reply": "Opening prescription scanner and dosage guide.",
        "patterns": ["open prescription scanner", "prescription", "scan prescription", "प्रिस्क्रिप्शन स्कैन करो", "पर्चा दिखाओ"]
    },
    # Dark Mode
    {
        "action": "THEME",
        "target": "dark",
        "speech_reply": "Switching to dark mode.",
        "patterns": ["switch to dark mode", "dark mode", "enable dark mode", "डार्क मोड चालू करो", "डार्क मोड"]
    },
    # Light Mode
    {
        "action": "THEME",
        "target": "light",
        "speech_reply": "Switching to light mode.",
        "patterns": ["switch to light mode", "light mode", "enable light mode", "लाइट मोड चालू करो", "लाइट मोड"]
    },
    # Language: Hindi
    {
        "action": "LANGUAGE",
        "target": "hi",
        "speech_reply": "भाषा हिंदी में बदल दी गई है।",
        "patterns": ["translate into hindi", "change language to hindi", "hindi language", "हिंदी में अनुवाद करो", "भाषा हिंदी करो", "हिंदी"]
    },
    # Language: English
    {
        "action": "LANGUAGE",
        "target": "en",
        "speech_reply": "Language changed to English.",
        "patterns": ["change language to english", "english language", "switch to english", "भाषा अंग्रेजी करो"]
    },
    # Speak / Read Aloud
    {
        "action": "SPEAK_REPORT",
        "target": None,
        "speech_reply": "Reading your simplified medical explanation aloud.",
        "patterns": ["read my report aloud", "read aloud", "read report", "मेरी रिपोर्ट पढ़कर सुनाओ", "पढ़कर सुनाओ"]
    },
    # Stop Speaking
    {
        "action": "STOP_SPEAK",
        "target": None,
        "speech_reply": "Audio playback stopped.",
        "patterns": ["stop speaking", "stop reading", "be quiet", "stop audio", "बोलना बंद करो", "चुप हो जाओ", "रुको"]
    },
    # Camera / Photo
    {
        "action": "CAMERA",
        "target": None,
        "speech_reply": "Opening camera to take a photo of your medical document.",
        "patterns": ["take a photo", "open camera", "capture photo", "take photo", "फोटो खींचो", "कैमरा खोलो"]
    },
    # Help
    {
        "action": "HELP",
        "target": None,
        "speech_reply": "You can say: Open dashboard, Upload report, Explain my report, Find hospitals, Switch to dark mode, or Change language.",
        "patterns": ["help me", "help", "commands", "what can you do", "मदद करो", "सहायता"]
    }
]

def parse_voice_command(spoken_text):
    """
    Match spoken transcript against known voice actions safely.
    Returns:
        dict: {"matched": bool, "action": str, "target": str, "reply": str}
    """
    clean_text = spoken_text.strip().lower()
    
    for cmd in COMMAND_MAPPINGS:
        for pat in cmd["patterns"]:
            if pat in clean_text:
                return {
                    "matched": True,
                    "action": cmd["action"],
                    "target": cmd["target"],
                    "speech_reply": cmd["speech_reply"],
                    "transcript": spoken_text
                }
                
    return {
        "matched": False,
        "action": "AI_CHAT",
        "target": None,
        "speech_reply": f"I heard: '{spoken_text}'. Asking MediR Assistant.",
        "transcript": spoken_text
    }
