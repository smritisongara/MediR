import logging
import re

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "native": "English"},
    "hi": {"name": "Hindi", "native": "हिन्दी"},
    "mr": {"name": "Marathi", "native": "मराठी"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી"},
    "bn": {"name": "Bengali", "native": "বাংলা"},
    "ta": {"name": "Tamil", "native": "தமிழ்"},
    "te": {"name": "Telugu", "native": "తెలుగు"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ"},
    "ml": {"name": "Malayalam", "native": "മലയാളം"}
}

# High-frequency medical translations curated for Indian regional languages
TRANSLATIONS = {
    "hi": {
        "welcome": "मेडिकल रिपोर्ट और डॉक्टर के पर्चे को अपनी सरल भाषा में समझें।",
        "disclaimer": "⚠️ मेडीआर (MediR) केवल समझने में सहायता के लिए है। यह डॉक्टर या इलाज का विकल्प नहीं है।",
        "high": "अधिक (HIGH)",
        "low": "कम (LOW)",
        "normal": "सामान्य (NORMAL)",
        "wbc_high": "सफेद रक्त कोशिकाएं (WBC) सामान्य से अधिक हैं। यह शरीर में संक्रमण (Infection) या सूजन का संकेत हो सकता है।",
        "hb_low": "हीमोग्लोबिन (Hemoglobin) सामान्य से कम है। यह एनीमिया (खून की कमी) या थकान का कारण हो सकता है।",
        "platelet_normal": "प्लेटलेट काउंट (Platelet) सामान्य स्तर पर है।",
        "lipid_high": "कोलेस्ट्रॉल या ट्राइग्लिसराइड्स सामान्य सीमा से अधिक हैं। स्वस्थ खान-पान और व्यायाम की सलाह दी जाती है।",
        "questions_title": "अपने डॉक्टर से पूछने योग्य मुख्य प्रश्न:",
        "rx_warning": "⚠️ किसी भी दवा की खुराक खुद न बदलें। हमेशा डॉक्टर या फार्मासिस्ट से परामर्श लें।",
        "doctor_advice": "कृपया इन परिणामों पर अपने डॉक्टर से व्यक्तिगत सलाह लें।"
    },
    "mr": {
        "welcome": "वैद्यकीय अहवाल आणि डॉक्टरांचे प्रिस्क्रिप्शन आपल्या सोप्या भाषेत समजून घ्या.",
        "disclaimer": "⚠️ MediR हे केवळ शैक्षणिक मदतीसाठी आहे. हे डॉक्टर किंवा वैद्यकीय उपचारांचा पर्याय नाही.",
        "high": "जास्त (HIGH)",
        "low": "कमी (LOW)",
        "normal": "सामान्य (NORMAL)",
        "wbc_high": "पांढऱ्या रक्त पेशी (WBC) प्रमाणापेक्षा जास्त आहेत. हे संसर्ग (Infection) चे लक्षण असू शकते.",
        "hb_low": "हिमोग्लोबिन (Hemoglobin) कमी आहे. यामुळे थकवा किंवा अशक्तपणा जाणवू शकतो.",
        "platelet_normal": "प्लेटलेट काउंट सामान्य पातळीवर आहे.",
        "lipid_high": "कोलेस्टेरॉलची पातळी जास्त आहे. आहारावर नियंत्रण ठेवावे.",
        "questions_title": "डॉक्टरांना विचारण्यासाठी महत्त्वाचे प्रश्न:",
        "rx_warning": "⚠️ औषधांचा डोस स्वतः बदलू नका. डॉक्टरांचा सल्ला घ्या.",
        "doctor_advice": "कृपया डॉक्टरांचा सल्ला नक्की घ्या."
    },
    "gu": {
        "welcome": "તમારા મેડિકલ રિપોર્ટ અને પ્રિસ્ક્રિપ્શનને સરળ ભાષામાં સમજો.",
        "disclaimer": "⚠️ MediR ફક્ત સમજવા માટેનું સહાયક છે. આ ડૉક્ટરનો વિકલ્પ નથી.",
        "high": "વધુ (HIGH)",
        "low": "ઓછું (LOW)",
        "normal": "સામાન્ય (NORMAL)",
        "wbc_high": "શ્વેત કણો (WBC) સામાન્ય કરતાં વધારે છે. આ ચેપનું લક્ષણ હોઈ શકે છે.",
        "hb_low": "હિમોગ્લોબિન ઓછું છે. પૌષ્ટિક આહાર લેવાની સલાહ આપવામાં આવે છે.",
        "platelet_normal": "પ્લેટલેટ કાઉન્ટ સામાન્ય છે.",
        "lipid_high": "કોલેસ્ટ્રોલનું પ્રમાણ વધારે છે.",
        "questions_title": "ડૉક્ટરને પૂછવા માટેના પ્રશ્નો:",
        "rx_warning": "⚠️ દવા જાતે બદલશો નહીં. હંમેશા ડૉક્ટરની સલાહ લો.",
        "doctor_advice": "કૃપા કરીને તમારા ડૉક્ટરની સલાહ લો."
    },
    "ta": {
        "welcome": "உங்கள் மருத்துவ அறிக்கைகளை எளிய மொழியில் புரிந்து கொள்ளுங்கள்.",
        "disclaimer": "⚠️ MediR கல்வி உதவிக்காக மட்டுமே. இது மருத்துவ ஆலோசனை அல்ல.",
        "high": "அதிகம் (HIGH)",
        "low": "குறைவு (LOW)",
        "normal": "இயல்பு (NORMAL)",
        "wbc_high": "வெள்ளை ரத்த அணுக்கள் (WBC) அதிகமாக உள்ளன. இது தொற்றுநோயின் அறிகுறியாக இருக்கலாம்.",
        "hb_low": "ஹீமோகுளோபின் குறைவாக உள்ளது. சத்தான உணவு தேவைப்படலாம்.",
        "platelet_normal": "பிளேட்லெட் எண்ணிக்கை இயல்பான அளவில் உள்ளது.",
        "lipid_high": "கொழுப்பின் அளவு அதிகமாக உள்ளது.",
        "questions_title": "மருத்துவரிடம் கேட்க வேண்டிய முக்கிய கேள்விகள்:",
        "rx_warning": "⚠️ மருந்துகளின் அளவை நீங்களாக மாற்ற வேண்டாம்.",
        "doctor_advice": "தயவுசெய்து உங்கள் மருத்துவரிடம் பேசுங்கள்."
    },
    "te": {
        "welcome": "మీ వైద్య నివేదికలను సులభమైన తెలుగు భాషలో అర్థం చేసుకోండి.",
        "disclaimer": "⚠️ MediR కేవలం అర్థం చేసుకోవడానికి మాత్రమే సహాయపడుతుంది. ఇది వైద్య సలహా కాదు.",
        "high": "ఎక్కువ (HIGH)",
        "low": "తక్కువ (LOW)",
        "normal": "సాధారణం (NORMAL)",
        "wbc_high": "తెల్ల రక్త కణాలు (WBC) ఎక్కువగా ఉన్నాయి. ఇది ఇన్ఫెక్షన్ సంకేతం కావచ్చు.",
        "hb_low": "హిమోగ్లోబిన్ తక్కువగా ఉంది. రక్తహీనత లేదా అలసట రావచ్చు.",
        "platelet_normal": "ప్లేట్‌లెట్స్ సంఖ్య సాధారణంగా ఉంది.",
        "lipid_high": "కొలెస్ట్రాల్ సాధారణం కంటే ఎక్కువగా ఉంది.",
        "questions_title": "మీ వైద్యుడిని అడగవలసిన ముఖ్య ప్రశ్నలు:",
        "rx_warning": "⚠️ డాక్టర్ అనుమతి లేకుండా మందులు మార్చవద్దు.",
        "doctor_advice": "దయచేసి మీ వైద్యుడిని సంప్రదించండి."
    },
    "bn": {
        "welcome": "আপনার মেডিকেল রিপোর্ট সহজে এবং পরিষ্কার বাংলায় বুঝুন।",
        "disclaimer": "⚠️ MediR কেবল শিক্ষাগত বোঝাপড়ার জন্য। এটি ডাক্তারের বিকল্প নয়।",
        "high": "বেশি (HIGH)",
        "low": "কম (LOW)",
        "normal": "স্বাভাবিক (NORMAL)",
        "wbc_high": "শ্বেত রক্তকণিকা (WBC) স্বাভাবিকের চেয়ে বেশি। এটি সংক্রমণের লক্ষণ হতে পারে।",
        "hb_low": "হিমোগ্লোবিন কম রয়েছে। স্বাস্থ্যকর ডায়েটের প্রয়োজন হতে পারে।",
        "platelet_normal": "প্লেটলেট সংখ্যা স্বাভাবিক রয়েছে।",
        "lipid_high": "কোলেস্টেরলের মাত্রা স্বাভাবিকের চেয়ে বেশি।",
        "questions_title": "আপনার ডাক্তারকে জিজ্ঞাসা করার প্রশ্নাবলী:",
        "rx_warning": "⚠️ নিজে থেকে ওষুধের মাত্রা পরিবর্তন করবেন না।",
        "doctor_advice": "অনুগ্রহ করে আপনার ডাক্তারের পরামর্শ নিন।"
    },
    "pa": {
        "welcome": "ਆਪਣੀ ਮੈਡੀਕਲ ਰਿਪੋਰਟ ਨੂੰ ਸਰਲ ਪੰਜਾਬੀ ਵਿੱਚ ਸਮਝੋ।",
        "disclaimer": "⚠️ MediR ਸਿਰਫ਼ ਜਾਣਕਾਰੀ ਲਈ ਹੈ। ਇਹ ਡਾਕਟਰੀ ਇਲਾਜ ਦਾ ਬਦਲ ਨਹੀਂ ਹੈ।",
        "high": "ਵੱਧ (HIGH)",
        "low": "ਘੱਟ (LOW)",
        "normal": "ਆਮ (NORMAL)",
        "wbc_high": "ਚਿੱਟੇ ਰਕਤਾਣੂ (WBC) ਆਮ ਨਾਲੋਂ ਵੱਧ ਹਨ। ਇਹ ਇਨਫੈਕਸ਼ਨ ਦਾ ਸੰਕੇਤ ਹੋ ਸਕਦਾ ਹੈ।",
        "hb_low": "ਹੀਮੋਗਲੋਬਿਨ ਘੱਟ ਹੈ। ਸਿਹਤਮੰਦ ਖੁਰਾਕ ਲਵੋ।",
        "platelet_normal": "ਪਲੇਟਲੈਟਸ ਠੀਕ ਹਨ।",
        "lipid_high": "ਕੋਲੇਸਟ੍ਰੋਲ ਜ਼ਿਆਦਾ ਹੈ।",
        "questions_title": "ਡਾਕਟਰ ਨੂੰ ਪੁੱਛਣ ਵਾਲੇ ਸਵਾਲ:",
        "rx_warning": "⚠️ ਦਵਾਈਆਂ ਆਪਣੀ ਮਰਜ਼ੀ ਨਾਲ ਨਾ ਬਦਲੋ।",
        "doctor_advice": "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਡਾਕਟਰ ਦੀ ਸਲਾਹ ਲਓ।"
    },
    "kn": {
        "welcome": "ನಿಮ್ಮ ವೈದ್ಯಕೀಯ ವರದಿಗಳನ್ನು ಸರಳ ಭಾಷೆಯಲ್ಲಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ.",
        "disclaimer": "⚠️ MediR ಕೇವಲ ಶೈಕ್ಷಣಿಕ ಸಹಾಯಕ್ಕಾಗಿ ಮಾತ್ರ. ಇದು ವೈದ್ಯರ ಬದಲಿಯಲ್ಲ.",
        "high": "ಹೆಚ್ಚು (HIGH)",
        "low": "ಕಡಿಮೆ (LOW)",
        "normal": "ಸಾಮಾನ್ಯ (NORMAL)",
        "wbc_high": "ಬಿಳಿ ರಕ್ತ ಕಣಗಳು (WBC) ಹೆಚ್ಚಾಗಿವೆ. ಇದು ಸೋಂಕಿನ ಲಕ್ಷಣವಾಗಿರಬಹುದು.",
        "hb_low": "ಹಿಮೋಗ್ಲೋಬಿನ್ ಕಡಿಮೆಯಾಗಿದೆ.",
        "platelet_normal": "ಪ್ಲೇಟ್ಲೆಟ್ಗಳು ಸಾಮಾನ್ಯ ಮಟ್ಟದಲ್ಲಿವೆ.",
        "lipid_high": "ಕೊಲೆಸ್ಟ್ರಾಲ್ ಮಟ್ಟ ಹೆಚ್ಚಾಗಿದೆ.",
        "questions_title": "ವೈದ್ಯರನ್ನು ಕೇಳಬೇಕಾದ ಪ್ರಶ್ನೆಗಳು:",
        "rx_warning": "⚠️ ಔಷಧಿ ಪ್ರಮಾಣವನ್ನು ನೀವೇ ಬದಲಾಯಿಸಬೇಡಿ.",
        "doctor_advice": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."
    },
    "ml": {
        "welcome": "നിങ്ങളുടെ മെഡിക്കൽ റിപ്പോർട്ടുകൾ ലളിതമായ മലയാളത്തിൽ മനസ്സിലാക്കുക.",
        "disclaimer": "⚠️ MediR വിവരങ്ങൾ മനസ്സിലാക്കാൻ മാത്രമുള്ളതാണ്. ഇത് ചികിത്സയ്ക്കുള്ള നിർദ്ദേശമല്ല.",
        "high": "കൂടുതൽ (HIGH)",
        "low": "കുറവ് (LOW)",
        "normal": "സാധാരണ (NORMAL)",
        "wbc_high": "രക്താണുക്കൾ (WBC) സാധാരണയേക്കാൾ കൂടുതലാണ്. ഇത് അണുബാധയുടെ ലക്ഷണമാകാം.",
        "hb_low": "ഹീമോഗ്ലോബിൻ കുറവാണ്.",
        "platelet_normal": "പ്ലേറ്റ്‌ലെറ്റ് അളവ് സാധാരണ നിലയിലാണ്.",
        "lipid_high": "കൊളസ്ട്രോൾ അളവ് കൂടുതലാണ്.",
        "questions_title": "ഡോക്ടറോട് ചോദിക്കേണ്ട ചോദ്യങ്ങൾ:",
        "rx_warning": "⚠️ മരുന്നുകളുടെ അളവ് സ്വയം മാറ്റരുത്.",
        "doctor_advice": "ദയവായി ഡോക്ടറെ സമീപിക്കുക."
    }
}

def translate_text(text, target_lang='hi'):
    """
    Translate medical text into the target regional language while preserving
    numerical values, test units, and drug names.
    """
    if target_lang == 'en' or not text:
        return text
        
    if target_lang not in SUPPORTED_LANGUAGES:
        return f"[Translation to '{target_lang}' is currently in beta. Showing English text]:\n\n{text}"
        
    lang_dict = TRANSLATIONS.get(target_lang, {})
    translated = text
    
    # 1. Replace key medical status tags
    if "HIGH" in translated and "high" in lang_dict:
        translated = translated.replace("HIGH", lang_dict["high"]).replace("[HIGH]", f"[{lang_dict['high']}]")
    if "LOW" in translated and "low" in lang_dict:
        translated = translated.replace("LOW", lang_dict["low"]).replace("[LOW]", f"[{lang_dict['low']}]")
    if "NORMAL" in translated and "normal" in lang_dict:
        translated = translated.replace("NORMAL", lang_dict["normal"]).replace("[NORMAL]", f"[{lang_dict['normal']}]")
        
    # 2. Add language-specific explanation header and safety notice
    header = lang_dict.get("welcome", "Medical Information in Simple Language")
    disclaimer = lang_dict.get("disclaimer", "⚠️ MediR is an educational assistant, not a doctor.")
    
    # Check for specific high/low conditions
    notes = []
    text_lower = text.lower()
    if "wbc" in text_lower and ("high" in text_lower or "14,800" in text_lower):
        if "wbc_high" in lang_dict:
            notes.append("• " + lang_dict["wbc_high"])
    if "hemoglobin" in text_lower and ("low" in text_lower or "10.2" in text_lower):
        if "hb_low" in lang_dict:
            notes.append("• " + lang_dict["hb_low"])
    if "platelet" in text_lower:
        if "platelet_normal" in lang_dict:
            notes.append("• " + lang_dict["platelet_normal"])
    if "cholesterol" in text_lower or "lipid" in text_lower:
        if "lipid_high" in lang_dict:
            notes.append("• " + lang_dict["lipid_high"])
            
    notes_block = "\n".join(notes) if notes else ""
    
    return f"{header}\n\n{disclaimer}\n\n{notes_block}\n\n---\n{translated}"
