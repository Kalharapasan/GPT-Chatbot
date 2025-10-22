from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import random

app = Flask(__name__)

# In-memory storage
chat_history = []

# Completely New Modern Interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat - Modern Interface</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: #0a0e27;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        
        /* Animated Grid Background */
        .grid-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(99, 102, 241, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99, 102, 241, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
            z-index: 0;
        }
        
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        
        /* Glowing Orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.6;
            z-index: 0;
            animation: float 15s infinite ease-in-out;
        }
        
        .orb1 {
            width: 300px;
            height: 300px;
            background: #6366f1;
            top: 10%;
            left: 20%;
        }
        
        .orb2 {
            width: 250px;
            height: 250px;
            background: #ec4899;
            bottom: 15%;
            right: 25%;
            animation-delay: 3s;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(50px, -50px) scale(1.1); }
        }
        
        /* Main Chat Container */
        .chat-wrapper {
            width: 100%;
            max-width: 900px;
            height: 85vh;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            border: 1px solid rgba(99, 102, 241, 0.2);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 1;
            overflow: hidden;
        }
        
        /* Top Bar */
        .top-bar {
            padding: 25px 30px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(236, 72, 153, 0.2));
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .top-bar-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .avatar-main {
            width: 55px;
            height: 55px;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
            animation: glow 3s infinite;
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.6); }
            50% { box-shadow: 0 0 30px rgba(236, 72, 153, 0.8); }
        }
        
        .top-bar-info h1 {
            color: #fff;
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 3px;
        }
        
        .top-bar-info p {
            color: rgba(255, 255, 255, 0.6);
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.3); }
        }
        
        .top-bar-actions {
            display: flex;
            gap: 10px;
        }
        
        .action-btn {
            width: 40px;
            height: 40px;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
            color: #fff;
            font-size: 16px;
        }
        
        .action-btn:hover {
            background: rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
        }
        
        /* Messages Container */
        .messages-container {
            flex: 1;
            overflow-y: auto;
            padding: 25px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .messages-container::-webkit-scrollbar {
            width: 6px;
        }
        
        .messages-container::-webkit-scrollbar-track {
            background: rgba(99, 102, 241, 0.1);
        }
        
        .messages-container::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.5);
            border-radius: 10px;
        }
        
        /* Welcome Screen */
        .welcome-screen {
            text-align: center;
            padding: 60px 20px;
            color: #fff;
        }
        
        .welcome-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .welcome-screen h2 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .welcome-screen p {
            font-size: 16px;
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.8;
            max-width: 500px;
            margin: 0 auto 30px;
        }
        
        /* Quick Suggestions */
        .suggestions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-top: 20px;
        }
        
        .suggestion-card {
            padding: 15px 20px;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 15px;
            color: #fff;
            cursor: pointer;
            transition: all 0.3s;
            text-align: left;
            font-size: 14px;
        }
        
        .suggestion-card:hover {
            background: rgba(99, 102, 241, 0.2);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        }
        
        .suggestion-icon {
            font-size: 24px;
            margin-bottom: 8px;
            display: block;
        }
        
        /* Message Bubbles */
        .message-row {
            display: flex;
            gap: 12px;
            animation: slideUp 0.4s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message-row.user {
            flex-direction: row-reverse;
        }
        
        .message-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        
        .message-row.bot .message-avatar {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }
        
        .message-row.user .message-avatar {
            background: linear-gradient(135deg, #ec4899, #f59e0b);
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
        }
        
        .message-bubble {
            max-width: 75%;
            padding: 15px 20px;
            border-radius: 18px;
            font-size: 15px;
            line-height: 1.6;
        }
        
        .message-row.bot .message-bubble {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #fff;
        }
        
        .message-row.user .message-bubble {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: #fff;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        .message-time {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.5);
            margin-top: 5px;
            padding: 0 5px;
        }
        
        .message-row.user .message-time {
            text-align: right;
        }
        
        /* Typing Animation */
        .typing-row {
            display: none;
            gap: 12px;
            align-items: center;
        }
        
        .typing-row.active {
            display: flex;
        }
        
        .typing-bubble {
            padding: 15px 20px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 18px;
            display: flex;
            gap: 6px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background: #6366f1;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.7; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
        
        /* Input Area */
        .input-area {
            padding: 25px;
            background: rgba(15, 23, 42, 0.95);
            border-top: 1px solid rgba(99, 102, 241, 0.2);
        }
        
        .input-box {
            display: flex;
            gap: 12px;
            align-items: center;
            background: rgba(30, 41, 59, 0.8);
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 20px;
            padding: 5px 5px 5px 20px;
            transition: all 0.3s;
        }
        
        .input-box:focus-within {
            border-color: #6366f1;
            box-shadow: 0 0 25px rgba(99, 102, 241, 0.3);
        }
        
        .input-box input {
            flex: 1;
            background: transparent;
            border: none;
            color: #fff;
            font-size: 15px;
            outline: none;
            padding: 12px 0;
            font-family: 'Poppins', sans-serif;
        }
        
        .input-box input::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }
        
        .send-button {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border: none;
            border-radius: 50%;
            color: #fff;
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4);
        }
        
        .send-button:hover:not(:disabled) {
            transform: scale(1.1) rotate(15deg);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6);
        }
        
        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .input-footer {
            text-align: center;
            margin-top: 12px;
            font-size: 12px;
            color: rgba(255, 255, 255, 0.5);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .chat-wrapper {
                height: 100vh;
                border-radius: 0;
            }
            
            .top-bar-info h1 {
                font-size: 18px;
            }
            
            .welcome-screen h2 {
                font-size: 28px;
            }
            
            .suggestions {
                grid-template-columns: 1fr;
            }
            
            .message-bubble {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <!-- Background Effects -->
    <div class="grid-background"></div>
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    
    <!-- Main Chat -->
    <div class="chat-wrapper">
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="top-bar-left">
                <div class="avatar-main">🤖</div>
                <div class="top-bar-info">
                    <h1>AI Assistant</h1>
                    <p>
                        <span class="pulse-dot"></span>
                        Online & Ready to Help
                    </p>
                </div>
            </div>
            <div class="top-bar-actions">
                <button class="action-btn" onclick="exportChat()" title="Export">💾</button>
                <button class="action-btn" onclick="clearChat()" title="Clear">🗑️</button>
            </div>
        </div>
        
        <!-- Messages -->
        <div class="messages-container" id="messagesContainer">
            <div class="welcome-screen">
                <div class="welcome-icon">✨</div>
                <h2>Welcome to AI Chat</h2>
                <p>I'm your intelligent assistant, ready to help with anything you need. Ask questions, get advice, or just chat!</p>
                
                <div class="suggestions">
                    <div class="suggestion-card" onclick="sendQuickMessage('Hello! How are you today?')">
                        <span class="suggestion-icon">👋</span>
                        Start with a greeting
                    </div>
                    <div class="suggestion-card" onclick="sendQuickMessage('What can you help me with?')">
                        <span class="suggestion-icon">💡</span>
                        Explore capabilities
                    </div>
                    <div class="suggestion-card" onclick="sendQuickMessage('Tell me something interesting')">
                        <span class="suggestion-icon">🌟</span>
                        Get a fun fact
                    </div>
                    <div class="suggestion-card" onclick="sendQuickMessage('Help me with coding')">
                        <span class="suggestion-icon">💻</span>
                        Coding assistance
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Typing Indicator -->
        <div class="typing-row" id="typingIndicator">
            <div class="message-avatar" style="background: linear-gradient(135deg, #6366f1, #8b5cf6);">
                🤖
            </div>
            <div class="typing-bubble">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        
        <!-- Input Area -->
        <div class="input-area">
            <div class="input-box">
                <input 
                    type="text" 
                    id="messageInput" 
                    placeholder="Type your message..." 
                    onkeypress="handleKeyPress(event)"
                    autocomplete="off"
                >
                <button class="send-button" id="sendBtn" onclick="sendMessage()">
                    ➤
                </button>
            </div>
            <div class="input-footer" id="inputFooter">
                💬 Ready to chat
            </div>
        </div>
    </div>

    <script>
        let messageCount = 0;
        
        function addMessage(type, text) {
            const container = document.getElementById('messagesContainer');
            const welcome = container.querySelector('.welcome-screen');
            if (welcome && messageCount === 0) {
                welcome.style.display = 'none';
            }
            
            const messageRow = document.createElement('div');
            messageRow.className = `message-row ${type}`;
            
            const time = new Date().toLocaleTimeString('en-US', {
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
            });
            
            const avatar = type === 'bot' ? '🤖' : '👤';
            
            messageRow.innerHTML = `
                <div class="message-avatar">${avatar}</div>
                <div>
                    <div class="message-bubble">${text}</div>
                    <div class="message-time">${time}</div>
                </div>
            `;
            
            container.appendChild(messageRow);
            container.scrollTop = container.scrollHeight;
            messageCount++;
            updateFooter();
        }
        
        function showTyping() {
            const typing = document.getElementById('typingIndicator');
            typing.classList.add('active');
            const container = document.getElementById('messagesContainer');
            typing.style.padding = '0 25px';
            container.parentElement.insertBefore(typing, container.nextSibling);
        }
        
        function hideTyping() {
            document.getElementById('typingIndicator').classList.remove('active');
        }
        
        function updateFooter() {
            const footer = document.getElementById('inputFooter');
            footer.textContent = `💬 ${messageCount} message${messageCount !== 1 ? 's' : ''} exchanged`;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage('user', message);
            input.value = '';
            
                // Disable the send button and show typing indicator
                const sendBtn = document.getElementById('sendBtn');
                sendBtn.disabled = true;
                showTyping();

                try {
                    const response = await fetch('/send', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });

                    // If server returned a non-OK response, try to read the text and throw
                    if (!response.ok) {
                        const errText = await response.text();
                        throw new Error(errText || 'Server error');
                    }

                    const data = await response.json();

                    // Always hide typing and re-enable the button even if adding message fails
                    hideTyping();
                    addMessage('bot', data && data.response ? data.response : 'Sorry, no response from server.');
                } catch (error) {
                    hideTyping();
                    console.error('Error sending message:', error);
                    addMessage('bot', 'Sorry — something went wrong. Please try again.');
                } finally {
                    sendBtn.disabled = false;
                }
        }
        
        function sendQuickMessage(message) {
            document.getElementById('messageInput').value = message;
            sendMessage();
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function exportChat() {
            try {
                const response = await fetch('/export');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `chat_${new Date().toISOString().split('T')[0]}.json`;
                a.click();
            } catch (error) {
                console.error('Export error:', error);
            }
        }
        
        async function clearChat() {
            if (confirm('Clear all messages?')) {
                try {
                    await fetch('/clear', {method: 'POST'});
                    const container = document.getElementById('messagesContainer');
                    container.innerHTML = `
                        <div class="welcome-screen">
                            <div class="welcome-icon">✨</div>
                            <h2>Welcome to AI Chat</h2>
                            <p>I'm your intelligent assistant, ready to help with anything you need. Ask questions, get advice, or just chat!</p>
                            
                            <div class="suggestions">
                                <div class="suggestion-card" onclick="sendQuickMessage('Hello! How are you today?')">
                                    <span class="suggestion-icon">👋</span>
                                    Start with a greeting
                                </div>
                                <div class="suggestion-card" onclick="sendQuickMessage('What can you help me with?')">
                                    <span class="suggestion-icon">💡</span>
                                    Explore capabilities
                                </div>
                                <div class="suggestion-card" onclick="sendQuickMessage('Tell me something interesting')">
                                    <span class="suggestion-icon">🌟</span>
                                    Get a fun fact
                                </div>
                                <div class="suggestion-card" onclick="sendQuickMessage('Help me with coding')">
                                    <span class="suggestion-icon">💻</span>
                                    Coding assistance
                                </div>
                            </div>
                        </div>
                    `;
                    messageCount = 0;
                    updateFooter();
                } catch (error) {
                    console.error('Clear error:', error);
                }
            }
        }
    </script>
</body>
</html>
'''

class AdvancedAIBot:
    """Enhanced AI bot"""
    
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! 👋 I'm thrilled to chat with you! How can I assist you today?",
                "Hi there! 😊 Welcome! What brings you here today?",
                "Hey! Great to see you! I'm ready to help with anything you need! 🌟"
            ],
            'help': [
                "I'm here to help! 🆘 I can answer questions, explain concepts, help with coding, creative writing, and much more. What interests you?",
                "I'd love to assist! 💡 I specialize in answering questions, providing explanations, coding help, and creative tasks. How can I support you?"
            ],
            'ai': [
                "Artificial Intelligence is fascinating! 🤖 It's about creating machines that can learn, reason, and solve problems like humans. What aspect interests you?",
                "AI is transforming our world! 🌍 From machine learning to neural networks, it's an exciting field. Want to know more about a specific area?"
            ],
            'technical': [
                "Great technical question! 💻 I love helping with code. What specific technology or problem are you working on?",
                "Let's dive into the technical details! 🔧 I can help with programming, algorithms, debugging, and more. What do you need?"
            ],
            'default': [
                "That's an interesting topic! 🤔 Let me share some insights... What would you like to know more about?",
                "Great question! 💭 I'm here to provide helpful information. Could you tell me more about what you're looking for?"
            ]
        }
    
    def get_response(self, message):
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.responses['greeting'])
        elif any(word in msg_lower for word in ['help', 'assist', 'support']):
            return random.choice(self.responses['help'])
        elif any(word in msg_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
            return random.choice(self.responses['ai'])
        elif any(word in msg_lower for word in ['code', 'program', 'python', 'javascript', 'coding']):
            return random.choice(self.responses['technical'])
        elif any(word in msg_lower for word in ['thank', 'thanks']):
            return "You're very welcome! 😊 Happy to help anytime! Feel free to ask more questions!"
        else:
            return f"Interesting! You mentioned '{message}'. {random.choice(self.responses['default'])}"

ai_bot = AdvancedAIBot()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '')
    
    user_msg = {
        'type': 'user',
        'text': user_message,
        'timestamp': datetime.now().strftime('%I:%M:%S %p')
    }
    chat_history.append(user_msg)
    
    ai_response = ai_bot.get_response(user_message)
    bot_msg = {
        'type': 'bot',
        'text': ai_response,
        'timestamp': datetime.now().strftime('%I:%M:%S %p')
    }
    chat_history.append(bot_msg)
    
    return jsonify({
        'success': True,
        'response': ai_response
    })

@app.route('/export')
def export_data():
    from flask import Response
    
    export_obj = {
        'export_date': datetime.now().isoformat(),
        'total_messages': len(chat_history),
        'messages': chat_history
    }
    
    json_data = json.dumps(export_obj, indent=2)
    return Response(
        json_data,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=chat_data.json'}
    )

@app.route('/clear', methods=['POST'])
def clear_chat():
    chat_history.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 AI Chat Interface Starting...")
    print("=" * 50)
    print("✨ Modern Chat Interface")
    print("🌐 Open: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)