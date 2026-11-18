/**
 * MediR AI - Educational Medical Chatbot
 */

let activeReportId = null;
let chatRecognition = null;
let isRecording = false;

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  activeReportId = urlParams.get('report_id');

  if (activeReportId) {
    const contextEl = document.getElementById('chatReportContext');
    if (contextEl) {
      contextEl.innerHTML = `<span class="badge bg-primary">Attached Context: Report #${activeReportId}</span>`;
    }
  }

  setupChatInput();
  setupSuggestedPrompts();
  setupChatMic();
});

function setupChatInput() {
  const sendBtn = document.getElementById('btnSendChat');
  const input = document.getElementById('chatInput');

  if (!sendBtn || !input) return;

  sendBtn.addEventListener('click', () => sendUserMessage());
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      sendUserMessage();
    }
  });
}

function sendUserMessage(presetText = null) {
  const input = document.getElementById('chatInput');
  const text = presetText || input.value.trim();
  if (!text) return;

  if (!presetText) input.value = '';

  appendMessage('user', text);

  // Show typing indicator
  const typingId = appendTypingIndicator();

  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question: text,
      report_id: activeReportId ? parseInt(activeReportId) : null
    })
  })
  .then(res => res.json())
  .then(data => {
    removeTypingIndicator(typingId);
    if (data.success) {
      appendMessage('ai', data.response);
    } else {
      appendMessage('ai', "Sorry, I encountered an issue processing your request.");
    }
  })
  .catch(() => {
    removeTypingIndicator(typingId);
    appendMessage('ai', "Connection error. Please check if the backend server is running.");
  });
}

function appendMessage(sender, text) {
  const container = document.getElementById('chatMessages');
  if (!container) return;

  const bubble = document.createElement('div');
  bubble.className = `chat-bubble chat-bubble-${sender}`;
  
  if (sender === 'ai') {
    // Format markdown bold
    const formatted = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
      
    bubble.innerHTML = `
      <div>${formatted}</div>
      <div class="mt-2 text-end">
        <button class="btn btn-sm btn-outline-secondary py-0 px-2 btn-speak-reply" title="Listen Aloud">
          <i class="bi bi-volume-up"></i>
        </button>
      </div>
    `;
    
    // Add voice playback listener
    const speakBtn = bubble.querySelector('.btn-speak-reply');
    if (speakBtn) {
      speakBtn.addEventListener('click', () => {
        speakText(text);
      });
    }
  } else {
    bubble.innerText = text;
  }

  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function appendTypingIndicator() {
  const container = document.getElementById('chatMessages');
  const id = 'typing_' + Date.now();
  const div = document.createElement('div');
  div.id = id;
  div.className = 'chat-bubble chat-bubble-ai text-muted fst-italic';
  div.innerHTML = '<i class="bi bi-three-dots"></i> MediR Assistant is typing...';
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function setupSuggestedPrompts() {
  document.querySelectorAll('.suggested-prompt-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      const q = btn.getAttribute('data-question') || btn.innerText;
      sendUserMessage(q);
    });
  });
}

// Speech-to-Text Microphone for Chat
function setupChatMic() {
  const micBtn = document.getElementById('btnChatMic');
  if (!micBtn) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    micBtn.style.display = 'none';
    return;
  }

  chatRecognition = new SpeechRecognition();
  chatRecognition.continuous = false;
  chatRecognition.interimResults = false;

  chatRecognition.onstart = () => {
    isRecording = true;
    micBtn.classList.add('btn-danger');
    micBtn.classList.remove('btn-outline-primary');
  };

  chatRecognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    document.getElementById('chatInput').value = transcript;
    sendUserMessage(transcript);
  };

  chatRecognition.onerror = () => {
    isRecording = false;
    micBtn.classList.remove('btn-danger');
    micBtn.classList.add('btn-outline-primary');
  };

  chatRecognition.onend = () => {
    isRecording = false;
    micBtn.classList.remove('btn-danger');
    micBtn.classList.add('btn-outline-primary');
  };

  micBtn.addEventListener('click', () => {
    if (isRecording) {
      chatRecognition.stop();
    } else {
      const currentLang = localStorage.getItem('medir_lang') || 'en';
      chatRecognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
      chatRecognition.start();
    }
  });
}
