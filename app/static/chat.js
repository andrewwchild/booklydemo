const chatEl = document.getElementById("chat");
const formEl = document.getElementById("form");
const inputEl = document.getElementById("input");
const statusEl = document.getElementById("status");
const suggestionsEl = document.getElementById("suggestions");

let sessionId = null;

async function init() {
  try {
    const res = await fetch("/health");
    const data = await res.json();
    statusEl.textContent = "Online";
    statusEl.classList.add("online");
  } catch {
    statusEl.textContent = "Offline";
  }

  appendMessage(
    "assistant",
    "Hello! I'm Bookly Support. I can assist with orders, returns, availability, book picks, shipping policies, or password resets. What can I help you with today?"
  );
}

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function showTyping() {
  const el = document.createElement("div");
  el.className = "typing";
  el.id = "typing";
  el.textContent = "Bookly Support is typing…";
  chatEl.appendChild(el);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function hideTyping() {
  document.getElementById("typing")?.remove();
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message) return;

  appendMessage("user", message);
  inputEl.value = "";
  inputEl.disabled = true;
  formEl.querySelector("button").disabled = true;
  showTyping();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    if (!res.ok) throw new Error(await res.text());

    const data = await res.json();
    sessionId = data.session_id;
    hideTyping();
    appendMessage("assistant", data.reply);
  } catch (err) {
    hideTyping();
    appendMessage("assistant", "Sorry, something went wrong. Please try again in a moment.");
    console.error(err);
  } finally {
    inputEl.disabled = false;
    formEl.querySelector("button").disabled = false;
    inputEl.focus();
  }
}

formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(inputEl.value);
});

suggestionsEl.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-msg]");
  if (btn) sendMessage(btn.dataset.msg);
});

init();
