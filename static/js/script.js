const autoResponses = {
    welcome: ["Hello! 👋 How can I help?", "Hi there! Ask me anything!", "Welcome! 😊"],
    confirmation: ["Got it! Checking that for you.", "Okay, I'll process that.", "Thanks! I'll get back to you shortly."],
    clarification: ["Could you rephrase that?", "I didn't quite catch that. Please clarify.", "Can you provide more info?"],
    farewell: ["Thank you! Come back anytime. 😊", "Glad to help! Reach out anytime.", "Goodbye! Have a great day!"],
    wasteHelp: ["Need help classifying waste?", "Got waste disposal questions? Let me know!", "Ask me about recycling or composting!"],
    aboutUs: ["We are a team committed to sustainable waste management. Let me know if you'd like to learn more!", "Our goal is to help communities with effective waste disposal solutions. How can we assist you?"],
    contactSupport: ["You can contact our support team at support@wastemgmt.com. We're here to help!", "If you need assistance, email us at support@wastemgmt.com. Our team is happy to assist."],
    help: ["I'm here to assist you with waste classification, recycling tips, and composting questions! Ask me anything!", "Need help with waste management or our services? I'm ready to help!"]
};

function getRandomMessage(category) {
    return autoResponses[category][Math.floor(Math.random() * autoResponses[category].length)];
}

function toggleChat() {
    document.getElementById("Icon").style.display = "none";
    const chatWindow = document.getElementById('chatbotWindow');
    chatWindow.style.display = chatWindow.style.display === 'block' ? 'none' : 'block';

    if (chatWindow.style.display === 'block') {
        displayMessage('bot', getRandomMessage('welcome'));
        displayOptions();
    }
}
function closeChat() {
    const chatWindow = document.getElementById('chatbotWindow');
    chatWindow.style.display = 'none';
    
    document.getElementById("Icon").style.display = 'block';
}
window.addEventListener('click', function(event) {
    const icon = document.getElementById("Icon");
    const chatWindow = document.getElementById('chatbotWindow');
    if (!chatWindow.contains(event.target) && !icon.contains(event.target)) {
        chatWindow.style.display = 'none';
        icon.style.display = 'block';
    }
});

function displayMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageDiv.textContent = message;
    document.getElementById('chatbotMessages').appendChild(messageDiv);
    document.getElementById('chatbotMessages').scrollTop = document.getElementById('chatbotMessages').scrollHeight;
}

function displayOptions() {
    const optionContainer = document.createElement('div');
    optionContainer.className = 'option-buttons';

    const options = [
        { text: 'Classify waste', callback: () => handleOptionClick('wasteHelp') },
        { text: 'About Us', callback: () => handleOptionClick('aboutUs') },
        { text: 'Contact Support', callback: () => handleOptionClick('contactSupport') },
        { text: 'Help', callback: () => handleOptionClick('help') },
    ];

    options.forEach(option => {
        const button = document.createElement('button');
        button.className = 'option-button';
        button.textContent = option.text;
        button.onclick = option.callback;
        optionContainer.appendChild(button);
    });

    document.getElementById('chatbotMessages').appendChild(optionContainer);
    document.getElementById('chatbotMessages').scrollTop = document.getElementById('chatbotMessages').scrollHeight;
}

function handleOptionClick(category) {
    displayMessage('user', ` ${category}`);
    displayMessage('bot', getRandomMessage(category));

    if (category === 'wasteHelp') {
        const classificationOptions = [
            { text: 'Plastic Waste', callback: () => handleWasteClassification('plastic') },
            { text: 'Organic Waste', callback: () => handleWasteClassification('organic') },
            { text: 'E-Waste', callback: () => handleWasteClassification('ewaste') },
            { text: 'Recycling Tips', callback: () => displayMessage('bot', "Recycling is the process of converting waste materials into reusable materials. Always separate recyclables from trash!") },
            { text: 'Composting Tips', callback: () => displayMessage('bot', "Composting is a natural process of recycling organic matter like food scraps and yard waste. It helps reduce landfill waste and enrich soil!") }
        ];

        const optionContainer = document.createElement('div');
        optionContainer.className = 'option-buttons';
        classificationOptions.forEach(option => {
            const button = document.createElement('button');
            button.className = 'option-button';
            button.textContent = option.text;
            button.onclick = option.callback;
            optionContainer.appendChild(button);
        });

        document.getElementById('chatbotMessages').appendChild(optionContainer);
        document.getElementById('chatbotMessages').scrollTop = document.getElementById('chatbotMessages').scrollHeight;
    }
}

function handleWasteClassification(wasteType) {
    let responseMessage = '';
    switch (wasteType) {
        case 'plastic':
            responseMessage = "Plastic waste includes items like plastic bottles, bags, and containers. These should be separated and placed in your recycling bin.";
            break;
        case 'organic':
            responseMessage = "Organic waste consists of food scraps, yard waste, and other biodegradable materials. These can be composted at home or disposed of in a compost bin.";
            break;
        case 'ewaste':
            responseMessage = "E-waste includes old electronics like phones, computers, and televisions. These should be taken to a recycling center that specializes in electronic waste.";
            break;
        default:
            responseMessage = "I'm not sure about that type of waste. Can you clarify?";
    }

    displayMessage('bot', responseMessage);
}
