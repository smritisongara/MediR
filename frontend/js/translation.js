/**
 * MediR AI - Multilingual Translation Studio
 */

document.addEventListener('DOMContentLoaded', () => {
  setupTranslationStudio();
});

function setupTranslationStudio() {
  const translateBtn = document.getElementById('btnTranslateStudio');
  const sourceText = document.getElementById('studioSourceText');
  const targetLangSelect = document.getElementById('studioTargetLang');
  const outputBox = document.getElementById('studioOutputText');
  const speakBtn = document.getElementById('btnStudioSpeak');
  const sampleBtn = document.getElementById('btnStudioLoadSample');

  if (!translateBtn || !sourceText || !targetLangSelect) return;

  translateBtn.addEventListener('click', () => {
    const text = sourceText.value.trim();
    if (!text) {
      alert("Please enter medical text to translate.");
      return;
    }

    const lang = targetLangSelect.value;
    outputBox.innerText = "Translating medical text...";

    fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text, target_lang: lang })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        outputBox.innerText = data.translated_text;
      } else {
        outputBox.innerText = "Translation error: " + data.error;
      }
    })
    .catch(() => {
      outputBox.innerText = "Failed to communicate with translation service.";
    });
  });

  if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
      sourceText.value = (
        "Laboratory Findings:\n"
        "Total Leucocyte Count (WBC): 14,800 /mcL [HIGH]\n"
        "Hemoglobin: 10.2 g/dL [LOW]\n"
        "Platelet Count: 220,000 /mcL [NORMAL]\n\n"
        "Doctor's Instruction:\n"
        "Take prescribed antibiotic Amoxicillin 500mg 3 times a day strictly after meals. "
        "Stay hydrated and complete full 5 days course. Avoid self-medicating."
      );
    });
  }

  if (speakBtn) {
    speakBtn.addEventListener('click', () => {
      const text = outputBox.innerText;
      if (!text || text === "Translated text will appear here...") return;
      const lang = targetLangSelect.value;
      speakText(text, lang);
    });
  }
}
