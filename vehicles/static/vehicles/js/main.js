// Smart Car Service - main JS file

document.addEventListener('DOMContentLoaded', function () {
    const sendBtn = document.getElementById('send-btn');
    const input = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');

    if (sendBtn) {
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
            addMessage(data.reply || 'Error happened, try again.', 'ai');
        }

        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // Scroll-reveal animation
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.15 });

        reveals.forEach(function (el) {
            observer.observe(el);
        });
    }
});

// Landing page parallax effect (mouse-move)
document.addEventListener('mousemove', function (e) {
    const icons = document.querySelectorAll('.floating-icon');
    if (!icons.length) return;
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    icons.forEach(function (icon, i) {
        const factor = (i + 1) * 0.6;
        icon.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
    });
});