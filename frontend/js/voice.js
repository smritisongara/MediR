/**
 * MediR AI - Dedicated Voice Assistant Studio Page
 */

document.addEventListener('DOMContentLoaded', () => {
  setupDedicatedVoiceControls();
});

function setupDedicatedVoiceControls() {
  const micBtn = document.getElementById('btnDedicatedVoiceMic');
  const statusEl = document.getElementById('dedicatedVoiceStatus');
  const transcriptEl = document.getElementById('dedicatedTranscript');
  const replyEl = document.getElementById('dedicatedVoiceReply');
  const waveBox = document.getElementById('dedicatedSoundWave');

  if (!micBtn) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    statusEl.innerText = "Speech recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.";
    micBtn.disabled = true;
    return;
  }

  const voiceRec = new SpeechRecognition();
  voiceRec.continuous = false;
  voiceRec.interimResults = false;

  let active = false;

  voiceRec.onstart = () => {
    active = true;
    statusEl.innerText = "Listening... Speak your command in English or Hindi.";
    micBtn.classList.add('listening');
    if (waveBox) waveBox.classList.add('listening');
  };

  voiceRec.onresult = (e) => {
    const text = e.results[0][0].transcript;
    transcriptEl.innerText = `"${text}"`;
    statusEl.innerText = "Command received. Processing...";

    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: text, is_voice: true })
    })
    .then(res => res.json())
    .then(data => {
      if (data.is_command && data.command) {
        const cmd = data.command;
        replyEl.innerText = cmd.speech_reply;
        speakText(cmd.speech_reply);
        statusEl.innerText = "Action Executed!";
        setTimeout(() => executeVoiceAction(cmd), 1500);
      } else {
        const r = data.response || "Command answered.";
        replyEl.innerText = r;
        speakText(r);
        statusEl.innerText = "Response completed.";
      }
    })
    .catch(() => {
      statusEl.innerText = "Error processing command.";
    });
  };

  voiceRec.onerror = (e) => {
    active = false;
    micBtn.classList.remove('listening');
    if (waveBox) waveBox.classList.remove('listening');
    statusEl.innerText = `Microphone error: ${e.error}. Tap to try again.`;
  };

  voiceRec.onend = () => {
    active = false;
    micBtn.classList.remove('listening');
    if (waveBox) waveBox.classList.remove('listening');
  };

  micBtn.addEventListener('click', () => {
    if (active) {
      voiceRec.stop();
    } else {
      const currentLang = localStorage.getItem('medir_lang') || 'en';
      voiceRec.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
      voiceRec.start();
    }
  });

  // Setup click on voice command pills
  document.querySelectorAll('.voice-command-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      const cmdText = pill.getAttribute('data-cmd');
      transcriptEl.innerText = `"${cmdText}"`;
      processSpokenCommand(cmdText);
    });
  });
}
