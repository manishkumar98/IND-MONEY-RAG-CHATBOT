const BACKEND_URL = "https://ind-money-rag-chatbot-36vp6kfeeuuesdzeprzetn.streamlit.app";

const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');

function appendMessage(role, content) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role === 'user' ? 'user-bubble' : 'ai-bubble'}`;

    // Convert source links from answer into clickable links if role is AI
    let processedContent = content;
    if (role === 'ai') {
        // Simple regex or string search if backend returns HTML
        // Our backend already returns HTML for links, so we can just set innerHTML
        bubble.innerHTML = `<div class="bubble-content">${processedContent}</div>`;
    } else {
        bubble.textContent = processedContent;
    }

    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const query = userInput.value.trim();
    if (!query) return;

    // 1. Clear input and show user bubble
    userInput.value = '';
    appendMessage('user', query);

    // 2. Add 'typing' state
    const loadingBubble = document.createElement('div');
    loadingBubble.className = 'chat-bubble ai-bubble loading';
    loadingBubble.textContent = 'Analysing data...';
    chatContainer.appendChild(loadingBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // 3. Call Backend (Streamlit Cloud serves the API)
    try {
        const response = await fetch(`${BACKEND_URL}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        // Remove loading state and show answer
        chatContainer.removeChild(loadingBubble);
        appendMessage('ai', data.answer);
    } catch (error) {
        chatContainer.removeChild(loadingBubble);
        appendMessage('ai', "I'm having trouble connecting to my brain right now. Please ensure the backend is running correctly.");
        console.error('Error calling backend:', error);
    }
}

function sendSuggestion(text) {
    userInput.value = text;
    sendMessage();
}

function handleEnter(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}
