# MediR AI – AI-Powered Medical Communication Assistant

> **"Understand Better. Communicate Better. Live Better."**  
> *Developed for CURSORFLOW: AI Insights to Innovation Hackathon*

---

## 📌 Project Overview
**MediR AI** is an advanced, responsive, AI-powered healthcare communication platform designed to solve a critical problem facing millions of patients: **understanding complicated medical reports, prescriptions, and physician instructions in simple language and their preferred regional language.**

Medical documents are saturated with clinical jargon, abbreviations (CBC, HbA1c, ESR, TLC), and reference bounds that induce panic or lead to mismanaged health. **MediR** solves this by uniting OCR extraction, AI clinical terminology simplification, multilingual translation across 10 Indian regional languages, text-to-speech audio, voice command navigation, an interactive nearby hospital finder, and camera/photo scanning.

---

## 🏗️ System Architecture

```text
                                +---------------------------+
                                |  Patient / User (Browser) |
                                +-------------+-------------+
                                              |
                   +--------------------------+--------------------------+
                   |                                                     |
                   v                                                     v
      [Frontend UI / Client]                                   [Web Speech & Geolocation]
   - HTML5, CSS3, JavaScript                                - SpeechRecognition (Voice Command)
   - Bootstrap 5 Responsive UI                              - SpeechSynthesis (Text-to-Speech)
   - Leaflet OpenStreetMap                                  - Browser GPS Location
   - Light / Dark Theme & A11y                               - WebCam MediaDevices API
                   |                                                     |
                   +--------------------------+--------------------------+
                                              | HTTP / JSON REST APIs
                                              v
                                 +-------------------------+
                                 |   Flask Backend Server  |
                                 |      (Python 3.15)      |
                                 +------------+------------+
                                              |
               +------------------------------+------------------------------+
               |                              |                              |
               v                              v                              v
      [File & OCR Engine]            [Clinical AI Services]          [Database Layer]
   - PDF Text (pypdf)             - Value Bounds & Reference Range   - SQLite (database/medir.db)
   - Optical OCR & Blur Check     - Medical Terminology Glossary     - Users, Reports, Explanations
   - Camera Snapshot Decoder      - Multi-language Translation (10)  - Prescriptions, Chat History
   - Video Audio Transcription    - Chatbot Context Engine & Safety  - Secure Deletion & Privacy
```

---

## 🌟 Key Features

### 1. 📄 Medical Report Upload & OCR
- Supports **PDF, PNG, JPG, JPEG, and WEBP** documents.
- Automatically extracts lab values, tests, and clinical notes.
- Built-in image quality validator (detects blur, low resolution, extreme darkness/overexposure).

### 2. 🤖 AI Medical Simplification & Abnormal Flagging
- Identifies critical tests (Hemoglobin, WBC, Platelets, Cholesterol, Triglycerides, HDL, LDL, Fasting Sugar, HbA1c, etc.).
- Compares readings against clinical biological reference ranges.
- Clearly flags **`[HIGH]`** or **`[LOW]`** readings with plain-language explanations.
- Never invents missing data. Generates personalized **"Questions for Your Doctor"**.

### 3. 🌐 Multilingual Translation System (10 Regional Languages)
- Instant translation into:
  - **Hindi (हिन्दी)**
  - **Marathi (मराठी)**
  - **Gujarati (ગુજરાતી)**
  - **Bengali (বাংলা)**
  - **Tamil (தமிழ்)**
  - **Telugu (తెలుగు)**
  - **Punjabi (ਪੰਜਾਬੀ)**
  - **Kannada (ಕನ್ನಡ)**
  - **Malayalam (മലയാളം)**
  - **English**
- Preserves test numerical values, units, and drug names without alteration.

### 4. 🎙️ AI Voice Command Assistant (English & Hindi)
- Controls MediR hands-free via spoken commands using browser Web Speech recognition:
  - *"Open dashboard"* / *"डैशबोर्ड खोलो"*
  - *"Upload medical report"* / *"मेडिकल रिपोर्ट अपलोड करो"*
  - *"Explain my report"* / *"मेरी रिपोर्ट समझाओ"*
  - *"Translate into Hindi"* / *"हिंदी में अनुवाद करो"*
  - *"Read my report aloud"* / *"मेरी रिपोर्ट पढ़कर सुनाओ"*
  - *"Find nearby hospitals"* / *"मेरे पास के अस्पताल दिखाओ"*
  - *"Switch to dark mode"* / *"डार्क मोड चालू करो"*
  - *"Open prescription scanner"* / *"प्रिस्क्रिप्शन स्कैन करो"*

### 5. 🏥 Interactive Nearby Hospital Finder & Map
- Interactive map powered by **Leaflet OpenStreetMap** (no paid API key required).
- One-click GPS location detection or manual city selection (**New Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, Pune**).
- Displays hospital name, address, distance (km), contact telephone, rating, and 24/7 emergency care badges.
- Direct links to Google Maps driving directions and emergency 108/112 dialer.

### 6. 💊 Prescription Explainer & Dosage Guide
- Decodes medicine names, drug classes, timing, and dosage instructions.
- Includes strict safety guidance and pharmacist verification notices.

### 7. 📸 Camera & Photo Scanner
- Live viewfinder capture via webcam / phone camera.
- Snapshot preview, retake, brightness analysis, and instant OCR submission.

### 8. 🎥 Medical Video & Consultation Audio Analyzer
- Upload consultation video clips (MP4, WebM, MOV) to generate transcripts and key bulleted instructions.

### 9. 🌓 Light & Dark Mode
- Full theme switching with persistent CSS variables and local storage saving.

### 10. ♿ Accessibility Improvements
- Font size adjustment (`A+` / `A-`), high-contrast display mode, screen-reader labels, keyboard focus.

---

## 📂 Project Directory Structure

```text
C:\Users\hp\Desktop\MediR/
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Login, register, guest access
│   │   ├── upload.py            # PDF/image/camera upload & OCR
│   │   ├── explain.py           # AI medical simplification
│   │   ├── translate.py         # 10-language translation API
│   │   ├── chatbot.py           # Contextual medical Q&A
│   │   ├── prescription.py      # Prescription dosage parser
│   │   ├── history.py           # Report history & secure deletion
│   │   ├── hospitals.py         # Geolocation hospital search
│   │   └── video.py             # Video consultation analysis
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py        # Clinical values analyzer & glossary
│   │   ├── ocr_service.py       # Image OCR & quality analyzer
│   │   ├── pdf_service.py       # pypdf text extraction
│   │   ├── translation_service.py # Regional language engine
│   │   └── speech_service.py    # Voice commands mapping
│   ├── app.py                   # Flask server & static router
│   ├── config.py                # App configuration
│   ├── database.py              # SQLite3 database manager
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── css/
│   │   ├── style.css            # Medical design system & dark mode
│   │   ├── dashboard.css        # 12 cards, chat & camera layout
│   │   └── responsive.css       # Mobile & tablet layout
│   ├── js/
│   │   ├── main.js              # Universal i18n, theme & voice
│   │   ├── upload.js            # Drag-and-drop & camera handler
│   │   ├── explanation.js       # Report breakdown & audio TTS
│   │   ├── chatbot.js           # Interactive Q&A chat
│   │   ├── translation.js       # Dedicated translation studio
│   │   ├── voice.js             # Dedicated voice assistant page
│   │   ├── prescription.js      # Prescription scanner
│   │   ├── hospitals.js         # Leaflet map & GPS search
│   │   └── history.js           # Patient reports & deletion
│   ├── index.html               # Landing page
│   ├── login.html               # Authentication & demo patient
│   ├── dashboard.html           # 12-Card Patient Dashboard
│   ├── upload.html              # Upload & camera photo
│   ├── explanation.html         # Report explanation & audio
│   ├── chatbot.html             # Medical chatbot
│   ├── translation.html         # Translation studio
│   ├── voice.html               # Voice assistant
│   ├── prescription.html        # Prescription explainer
│   ├── hospitals.html           # Nearby hospital map
│   ├── history.html             # Saved reports
│   └── about.html               # Hackathon pitch & architecture
├── database/
│   └── medir.db                 # SQLite database
├── sample_data/                 # Preloaded anonymized test files
│   ├── sample_cbc_report.txt
│   ├── sample_lipid_profile.txt
│   ├── sample_prescription.txt
│   ├── sample_blood_test.pdf
│   └── sample_prescription.png
├── tests/
│   ├── test_api.py              # API endpoint unit tests
│   └── test_upload.py           # Upload & prescription tests
├── .env.example
├── .gitignore
├── README.md
├── run.py                       # Main server launcher
└── start.bat                    # Windows 1-click batch launcher
```

---

## 🚀 How to Run the Website (Step-by-Step in VS Code)

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Go to **File -> Open Folder...** and select:
   `C:\Users\hp\Desktop\MediR`
3. Open the integrated terminal (**Terminal -> New Terminal** or press ``Ctrl + ` ``).

### Step 2: Install Dependencies
In the terminal, run:
```bash
pip install -r backend/requirements.txt
```
*(All dependencies: `flask`, `flask-cors`, `python-dotenv`, `pypdf`, `pillow`, `requests`)*

### Step 3: Run the Application
Start the server by executing:
```bash
python run.py
```
*(Or double-click `start.bat` from File Explorer).*

You will see:
```text
======================================================================
           🏥 MediR AI - Medical Communication Assistant
      'Understand Better. Communicate Better. Live Better.'
        CURSORFLOW: AI Insights to Innovation Hackathon
======================================================================
[*] Initializing SQLite database...
[+] Database ready: database/medir.db

[🚀] Server is running!
[🌐] OPEN IN YOUR BROWSER: http://127.0.0.1:5000
```

### Step 4: Open in Your Browser
Open Chrome, Edge, or Firefox and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 How to Test Every Feature Manually

### 1. Test 1-Click Instant Demo Login
- Click **Login** in the top navbar.
- Click **"Instant Demo Patient Login"**.
- You will be immediately logged in as `demo_patient` and redirected to the **12-Card Dashboard**.

### 2. Test Medical Report Upload & Simplification
- Navigate to **Upload Report** (`/upload`).
- Under **Instant Hackathon Demo Testing**, click **"Load Sample Blood Test (CBC)"**.
- Notice how it immediately analyzes:
  - **Hemoglobin: 10.2 g/dL [LOW]**
  - **WBC: 14,800 /mcL [HIGH]**
  - **Platelets: 220,000 /mcL [NORMAL]**
- The system automatically redirects to `/explanation.html` displaying:
  - Plain language summary.
  - High/Low badges with standard reference ranges.
  - Questions to ask your doctor.
  - Medical terminology decoded.

### 3. Test Audio Text-to-Speech
- On `/explanation.html`, click the **Play** button in the audio player bar.
- Listen as your browser speaks the simplified medical explanation aloud.
- Use the **Pause**, **Resume**, **Stop**, and **Speed** controls.

### 4. Test Live Regional Translation
- On `/explanation.html`, change the **"Read In:"** dropdown from English to **हिन्दी (Hindi)**, **मराठी (Marathi)**, or **தமிழ் (Tamil)**.
- Notice how the summary updates in real-time while preserving lab numbers and units.
- Click **Play** to listen to the explanation read aloud in Hindi!

### 5. Test AI Medical Chatbot
- Click **"Ask AI Chatbot With This Report"** or open `/chatbot.html`.
- Click one of the quick question pills:
  - *"What does high WBC mean?"*
  - *"What questions should I ask my doctor?"*
- Or type your own question.
- Click the speaker button next to the AI reply to listen aloud.
- Click the **Microphone** icon to speak your question using voice!

### 6. Test Nearby Hospital Finder with Interactive Map
- Open **Nearby Hospitals** (`/hospitals.html`).
- Click **"Detect My GPS Location"** or pick a city like **New Delhi**, **Mumbai**, or **Bengaluru** from the dropdown.
- View hospital markers, 24/7 Emergency trauma badges, distance (km), telephone, and click **Directions** to route on Google Maps.

### 7. Test AI Voice Assistant
- Click the floating **Microphone Button** on the bottom right of any page (or go to `/voice.html`).
- Speak:
  - *"Open dashboard"* (Opens dashboard)
  - *"Switch to dark mode"* (Changes theme)
  - *"Find nearby hospitals"* (Opens map)
  - Or in Hindi: *"डैशबोर्ड खोलो"*, *"डार्क मोड चालू करो"*!

### 8. Test Prescription Explainer
- Go to `/prescription.html`.
- Click **"Load Sample Prescription (Rx)"**.
- See Amoxicillin, Paracetamol, and Cetirizine parsed with schedule, purpose, and pharmacist consult warning.

### 9. Test Report History & Deletion
- Go to **My Reports** (`/history.html`).
- View all processed reports.
- Click **"View"** to re-open any report.
- Click **"Delete"** to permanently wipe the report from database and disk.

---

## 🔒 Safety, Ethics & Privacy
- **Educational Only**: MediR is an educational communication assistant, not a doctor. It does not provide diagnoses or prescribe drugs.
- **Zero Hallucination**: Lab numbers, units, and medicine names are strictly extracted without fabrication.
- **Privacy First**: Patient data can be wiped by the user with 1-click. No patient data is shared publicly.

---

## 🏆 Hackathon Submission Details
- **Project Name:** MediR AI
- **Tagline:** *"Understand Better. Communicate Better. Live Better."*
- **Hackathon:** CURSORFLOW: AI Insights to Innovation
- **Author:** Solo Developer
#   M e d i R  
 