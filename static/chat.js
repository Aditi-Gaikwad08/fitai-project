/**
 * chat.js — FitAI Gym Buddy v2
 * Handles message sending, bot reply rendering, and UI interactions.
 * Communicates with Flask /api/chat endpoint via fetch().
 */

const chatWindow = document.getElementById('chatWindow');
const chatInput  = document.getElementById('chatInput');
const sendBtn    = document.getElementById('sendBtn');

// ── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Scroll chat window to the bottom.
 */
function scrollToBottom() {
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

/**
 * Append a message row to the chat window.
 * @param {string} text    - message text
 * @param {'user'|'bot'} sender
 */
function appendMessage(text, sender) {
  const row    = document.createElement('div');
  row.className = `msg-row ${sender}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = sender === 'bot' ? '🤖' : '🧑';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = text;

  if (sender === 'bot') {
    row.appendChild(avatar);
    row.appendChild(bubble);
  } else {
    row.appendChild(bubble);
    row.appendChild(avatar);
  }

  chatWindow.appendChild(row);
  scrollToBottom();
}

/**
 * Show a typing indicator (animated dots).
 * @returns {HTMLElement} the typing row (so we can remove it later)
 */
function showTyping() {
  const row    = document.createElement('div');
  row.className = 'msg-row bot';
  row.id = 'typingRow';

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = '🤖';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble typing-bubble';
  bubble.innerHTML = '<span></span><span></span><span></span>';

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatWindow.appendChild(row);
  scrollToBottom();
  return row;
}

/**
 * Remove the typing indicator.
 */
function removeTyping() {
  const row = document.getElementById('typingRow');
  if (row) row.remove();
}

// ── Core send logic ───────────────────────────────────────────────────────────

/**
 * Send a message to the /api/chat endpoint and display the reply.
 * @param {string} message - user message text
 */
async function sendMessage(message) {
  message = (message || '').trim();
  if (!message) return;

  // Show user message
  appendMessage(message, 'user');
  chatInput.value = '';
  sendBtn.disabled = true;
  chatInput.disabled = true;

  // Show typing indicator
  showTyping();

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    removeTyping();

    // Small delay for natural feel
    await new Promise(r => setTimeout(r, 200));
    appendMessage(data.reply || 'Sorry, I could not generate a response.', 'bot');

  } catch (err) {
    removeTyping();
    appendMessage('Connection error. Make sure Flask is running (python app.py).', 'bot');
    console.error('Chat error:', err);
  } finally {
    sendBtn.disabled = false;
    chatInput.disabled = false;
    chatInput.focus();
  }
}

// ── Event listeners ───────────────────────────────────────────────────────────

sendBtn.addEventListener('click', () => {
  sendMessage(chatInput.value);
});

chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage(chatInput.value);
  }
});

// ── Chip handler ──────────────────────────────────────────────────────────────

/**
 * Called inline from chip elements in chat.html.
 * @param {HTMLElement} el - the clicked chip
 */
function sendChip(el) {
  const text = el.dataset.msg || el.textContent.trim();
  sendMessage(text);
}

// ── Init ──────────────────────────────────────────────────────────────────────

// Focus input on page load
window.addEventListener('DOMContentLoaded', () => {
  chatInput.focus();
  scrollToBottom();
});