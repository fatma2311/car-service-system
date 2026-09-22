// Smart Car Service - main JS file
// Will be used later for the AI Agent chat widget and dynamic interactions
console.log("Smart Car Service loaded ✅");

// Smart Car Service - main JS file

document.addEventListener('DOMContentLoaded', function () {
    const sendBtn = document.getElementById('send-btn');
    const input = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');

    
    if (!sendBtn) return;

    function addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.textContent = text;
        msg.style.padding = '8px 12px';
        msg.style.borderRadius = '10px';
        msg.style.maxWidth = '80%';
        msg.style.whiteSpace = 'pre-line';
        if (sender === 'user') {
            msg.style.alignSelf = 'flex-end';
            msg.style.background = '#0f1729';
            msg.style.color = 'white';
        } else {
            msg.style.alignSelf = 'flex-start';
            msg.style.background = '#f0f0f0';
        }
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        input.value = '';

        const response = await fetch('/assistant/message/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text }),
        });

        const data = await response.json();
        addMessage(data.reply || 'Error Happened, Try Again', 'ai');
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });
});