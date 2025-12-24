const API_URL = "http://127.0.0.1:8000/message";

// Stores which phone conversation is currently open
let currentPhone = "";

// Runtime-only storage of all conversations
let conversations = {};

// Render conversation list ( left container)
// For every phone number created, display a chat item
function renderConversations() {
    const container = document.querySelector('.conversations');
    container.innerHTML = '';

    Object.keys(conversations).forEach(phone => {
        const conv = conversations[phone];

        // Create UI box for each conversation
        const div = document.createElement('div');
        div.className = `conversation-item ${phone === currentPhone ? 'active' : ''}`;
        div.innerHTML = `
            <div class="conversation-avatar">👤</div>
            <div class="conversation-info">
                <div class="conversation-phone">${phone}</div>
                <div class="conversation-time">
                    Last message: ${conv.lastMessage || 'No messages'}
                </div>
            </div>
        `;
        div.onclick = () => selectConversation(phone);
        container.appendChild(div);
    });
}

// Add new conversation
function addConversation() {
    const input = document.getElementById('new-phone');
    const phone = input.value.trim();

    // phone validation
    if (!phone) return alert("Please enter a phone number");
    if (!phone.startsWith("+407")) return alert("Phone must start with +407");

    // if phone conversation does not exist, create it
    if (!conversations[phone]) {
        conversations[phone] = {
            messages: [],
            lastMessage: "New conversation"
        };
        renderConversations();
        selectConversation(phone);
    } else {
    // else just open it
        selectConversation(phone);
    }

    input.value = "";
}

// Select conversation
function selectConversation(phone) {
    currentPhone = phone;
    // update header
    document.getElementById('current-phone').textContent = phone;
    document.getElementById('connection-status').textContent = 'online';
    document.getElementById('connection-status').style.color = '#25d366';

    // enable input
    const messageInput = document.getElementById('message');
    const sendButton = document.querySelector('.input-row button');

    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.placeholder = "Type your message...";

    // load chat
    loadMessages();
    renderConversations();

    setTimeout(() => messageInput.focus(), 100);
}

// Load chat messages
function loadMessages() {
    const chatBox = document.getElementById('chat-box');
    const conv = conversations[currentPhone];

    chatBox.innerHTML = '';

    if (!conv || conv.messages.length === 0) {
        chatBox.innerHTML = `
            <div class="message bot">Hello! This is a new conversation with ${currentPhone}. Please provide just the username.
            </div>
        `;
    } else {
        conv.messages.forEach(msg => {
            const div = document.createElement('div');
            div.className = `message ${msg.sender}`;
            div.textContent = msg.text;
            chatBox.appendChild(div);
        });
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Add message to conversation memory
function addMessage(text, sender) {
    if (!conversations[currentPhone]) {
        conversations[currentPhone] = { messages: [] };
    }

    const message = {
        text,
        sender,
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    };

    // save message in conversation history
    conversations[currentPhone].messages.push(message);
    // update preview text in sidebar
    conversations[currentPhone].lastMessage = text.substring(0, 30) + (text.length > 30 ? "..." : "");

    renderConversations();

    // display in chat UI
    const chatBox = document.getElementById('chat-box');
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message to backend
async function sendMessage() {
    const input = document.getElementById('message');
    const text = input.value.trim();

    if (!text || !currentPhone) return;

    // show user message
    addMessage(text, 'user');
    input.value = '';

    try {
        // request for FastAPI backend
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                from: currentPhone,
                text
            })
        });

        const data = await res.json();

        // give a small delay
        setTimeout(() => {
            addMessage(data.reply || "I received your message!", "bot");
        }, 400);

    } catch {
        addMessage("Could not connect to server...", 'bot');
    }
}

// Auto + for phone
document.getElementById('new-phone').addEventListener('input', e => {
    if (e.target.value && !e.target.value.startsWith('+')) {
        e.target.value = '+' + e.target.value;
    }
});

// Enter = send
document.getElementById('message').addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});

// focus input on phone bar
window.onload = () => {
    document.getElementById('new-phone').focus();
};