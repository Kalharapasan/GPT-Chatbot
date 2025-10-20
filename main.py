from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import re
import random

app = Flask(__name__)

chat_history = []
user_context = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced AI Chat Room</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .background-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 20s infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); }
            50% { transform: translateY(-100px) translateX(100px); }
        }
        .container {
            width: 95%;
            max-width: 1400px;
            height: 95vh;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.4);
            display: grid;
            grid-template-columns: 300px 1fr;
            overflow: hidden;
            position: relative;
            z-index: 1;
        }
        .sidebar {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            padding: 24px;
            color: white;
            overflow-y: auto;
        }
        .sidebar h2 {
            font-size: 20px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .stats-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            backdrop-filter: blur(10px);
        }
        .stats-card h3 {
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 8px;
        }
        .stats-card .value {
            font-size: 28px;
            font-weight: bold;
            color: #60a5fa;
        }
        .category-list {
            margin-top: 20px;
        }
        .category-item {
            padding: 10px;
            margin: 8px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .category-item:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(5px);
        }
        .category-item.active {
            background: #3b82f6;
        }
        .badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
        }
        .main-area {
            display: flex;
            flex-direction: column;
            background: #f8fafc;
        }
        .header {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 24px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 32px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .ai-status {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
        }
        .status-dot {
            width: 10px;
            height: 10px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .controls {
            padding: 20px 32px;
            background: white;
            border-bottom: 2px solid #e2e8f0;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            align-items: center;
        }
        .controls select, .controls input {
            padding: 10px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s;
        }
        .controls select:focus, .controls input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        .controls input[type="text"] {
            flex: 1;
            min-width: 200px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
        }
        .btn-success {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }
        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
        }
        .btn-danger {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }
        .chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 32px;
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        }
        .message {
            display: flex;
            margin-bottom: 24px;
            animation: slideIn 0.4s ease-out;
        }
        @keyframes slideIn {
            from { 
                opacity: 0; 
                transform: translateY(20px);
            }
            to { 
                opacity: 1; 
                transform: translateY(0);
            }
        }
        .message.user {
            flex-direction: row-reverse;
        }
        .message-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .message.bot .message-avatar {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        }
        .message.user .message-avatar {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        }
        .message-content {
            max-width: 65%;
            margin: 0 16px;
        }
        .message-bubble {
            padding: 16px 20px;
            border-radius: 18px;
            word-wrap: break-word;
            line-height: 1.6;
            position: relative;
        }
        .message.bot .message-bubble {
            background: white;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }
        .message.user .message-bubble {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
        }
        .message-meta {
            font-size: 12px;
            color: #64748b;
            margin-top: 8px;
            display: flex;
            gap: 12px;
            align-items: center;
        }
        .category-tag {
            background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            color: #6366f1;
        }
        .sentiment-badge {
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        }
        .sentiment-positive { background: #dcfce7; color: #16a34a; }
        .sentiment-neutral { background: #f3f4f6; color: #6b7280; }
        .sentiment-negative { background: #fee2e2; color: #dc2626; }
        .typing-indicator {
            display: none;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }
        .typing-indicator.active {
            display: flex;
        }
        .typing-dots {
            display: flex;
            gap: 6px;
        }
        .typing-dots span {
            width: 10px;
            height: 10px;
            background: #6366f1;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        .input-area {
            padding: 24px 32px;
            background: white;
            border-top: 2px solid #e2e8f0;
        }
        .input-container {
            display: flex;
            gap: 12px;
            align-items: center;
            background: #f8fafc;
            padding: 8px;
            border-radius: 28px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s;
        }
        .input-container:focus-within {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }
        .input-container input {
            flex: 1;
            padding: 14px 20px;
            border: none;
            background: transparent;
            font-size: 15px;
            outline: none;
        }
        .input-container button {
            padding: 14px 28px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 15px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .input-container button:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
        }
        .input-container button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .stats-footer {
            text-align: center;
            color: #64748b;
            font-size: 13px;
            margin-top: 12px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .quick-actions {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        .quick-action {
            padding: 8px 14px;
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .quick-action:hover {
            background: #6366f1;
            color: white;
            border-color: #6366f1;
            transform: translateY(-2px);
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body>
    <div class="background-animation" id="bgAnimation"></div>
    
    <div class="container">
        <!-- Sidebar -->
        <div class="sidebar">
            <h2>📊 Dashboard</h2>
            
            <div class="stats-card">
                <h3>Total Messages</h3>
                <div class="value" id="totalMessages">0</div>
            </div>
            
            <div class="stats-card">
                <h3>AI Responses</h3>
                <div class="value" id="aiResponses">0</div>
            </div>
            
            <div class="stats-card">
                <h3>Avg Response Time</h3>
                <div class="value" id="avgTime">0.8s</div>
            </div>
            
            <div class="category-list">
                <h3 style="margin-bottom: 12px; font-size: 16px;">Categories</h3>
                <div class="category-item active" onclick="filterByCategory('all')">
                    <span>🌐 All Messages</span>
                    <span class="badge" id="count-all">0</span>
                </div>
                <div class="category-item" onclick="filterByCategory('greeting')">
                    <span>👋 Greetings</span>
                    <span class="badge" id="count-greeting">0</span>
                </div>
                <div class="category-item" onclick="filterByCategory('question')">
                    <span>❓ Questions</span>
                    <span class="badge" id="count-question">0</span>
                </div>
                <div class="category-item" onclick="filterByCategory('help')">
                    <span>🆘 Help</span>
                    <span class="badge" id="count-help">0</span>
                </div>
                <div class="category-item" onclick="filterByCategory('technical')">
                    <span>💻 Technical</span>
                    <span class="badge" id="count-technical">0</span>
                </div>
                <div class="category-item" onclick="filterByCategory('creative')">
                    <span>🎨 Creative</span>
                    <span class="badge" id="count-creative">0</span>
                </div>
                <div class="category-item" onclick="filterByCategory('analysis')">
                    <span>📈 Analysis</span>
                    <span class="badge" id="count-analysis">0</span>
                </div>
            </div>
        </div>
        
        <!-- Main Area -->
        <div class="main-area">
            <div class="header">
                <h1>🤖 Advanced AI Assistant</h1>
                <div class="ai-status">
                    <div class="status-dot"></div>
                    <span>AI Online</span>
                </div>
            </div>
            
            <div class="controls">
                <select id="sortBy" onchange="loadMessages()">
                    <option value="time">⏱️ Sort by Time</option>
                    <option value="reverse">🔄 Latest First</option>
                    <option value="type">👤 Sort by Type</option>
                    <option value="category">📁 Sort by Category</option>
                </select>
                
                <input type="text" id="searchTerm" placeholder="🔍 Search messages..." onkeyup="loadMessages()">
                
                <button class="btn btn-success" onclick="exportData()">📥 Export</button>
                <button class="btn btn-danger" onclick="clearChat()">🗑️ Clear</button>
            </div>
            
            <div class="chat-area" id="chatArea">
                <div class="quick-actions">
                    <div class="quick-action" onclick="sendQuickMessage('Hello! How are you?')">👋 Say Hello</div>
                    <div class="quick-action" onclick="sendQuickMessage('What can you help me with?')">❓ Get Help</div>
                    <div class="quick-action" onclick="sendQuickMessage('Tell me something interesting')">💡 Random Fact</div>
                    <div class="quick-action" onclick="sendQuickMessage('Explain AI to me')">🤖 About AI</div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="message-avatar" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);">🤖</div>
                <div>
                    <div class="typing-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
            
            <div class="input-area">
                <div class="input-container">
                    <input type="text" id="messageInput" placeholder="Ask me anything... I'm here to help! 💬" onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()" id="sendBtn">Send 🚀</button>
                </div>
                <div class="stats-footer">
                    <span id="stats">Ready to chat</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Create animated background particles
        function createParticles() {
            const bg = document.getElementById('bgAnimation');
            for (let i = 0; i < 15; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.width = Math.random() * 80 + 20 + 'px';
                particle.style.height = particle.style.width;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = Math.random() * 20 + 10 + 's';
                bg.appendChild(particle);
            }
        }
        createParticles();
        
        function updateCategoryCounts(messages) {
            const counts = {};
            messages.forEach(msg => {
                counts[msg.category] = (counts[msg.category] || 0) + 1;
            });
            
            document.getElementById('count-all').textContent = messages.length;
            document.getElementById('count-greeting').textContent = counts.greeting || 0;
            document.getElementById('count-question').textContent = counts.question || 0;
            document.getElementById('count-help').textContent = counts.help || 0;
            document.getElementById('count-technical').textContent = counts.technical || 0;
            document.getElementById('count-creative').textContent = counts.creative || 0;
            document.getElementById('count-analysis').textContent = counts.analysis || 0;
            
            const botMessages = messages.filter(m => m.type === 'bot').length;
            document.getElementById('totalMessages').textContent = messages.length;
            document.getElementById('aiResponses').textContent = botMessages;
        }
        
        function filterByCategory(category) {
            document.querySelectorAll('.category-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.closest('.category-item').classList.add('active');
            
            const filterSelect = document.getElementById('sortBy');
            loadMessages(category);
        }
        
        function loadMessages(filterCat = null) {
            const sortBy = document.getElementById('sortBy').value;
            const searchTerm = document.getElementById('searchTerm').value;
            const filterCategory = filterCat || new URLSearchParams(window.location.search).get('filter') || 'all';
            
            fetch(`/messages?sort=${sortBy}&filter=${filterCategory}&search=${searchTerm}`)
                .then(res => res.json())
                .then(data => {
                    displayMessages(data.messages);
                    updateCategoryCounts(data.all_messages);
                    document.getElementById('stats').innerHTML = 
                        `<span>💬 Total: ${data.total}</span> <span>📊 Displayed: ${data.displayed}</span>`;
                });
        }
        
        function displayMessages(messages) {
            const chatArea = document.getElementById('chatArea');
            const quickActions = chatArea.querySelector('.quick-actions');
            chatArea.innerHTML = '';
            if (quickActions) chatArea.appendChild(quickActions);
            
            messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${msg.type}`;
                
                const sentimentClass = msg.sentiment ? `sentiment-${msg.sentiment}` : '';
                const sentimentBadge = msg.sentiment ? 
                    `<span class="sentiment-badge ${sentimentClass}">${msg.sentiment}</span>` : '';
                
                messageDiv.innerHTML = `
                    <div class="message-avatar">${msg.type === 'bot' ? '🤖' : '👤'}</div>
                    <div class="message-content">
                        <div class="message-bubble">${msg.text}</div>
                        <div class="message-meta">
                            <span>⏰ ${msg.timestamp}</span>
                            <span class="category-tag">${msg.category}</span>
                            ${sentimentBadge}
                        </div>
                    </div>
                `;
                chatArea.appendChild(messageDiv);
            });
            
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function showTypingIndicator() {
            document.getElementById('typingIndicator').classList.add('active');
        }
        
        function hideTypingIndicator() {
            document.getElementById('typingIndicator').classList.remove('active');
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            document.getElementById('sendBtn').disabled = true;
            showTypingIndicator();
            
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(res => res.json())
            .then(() => {
                input.value = '';
                setTimeout(() => {
                    hideTypingIndicator();
                    loadMessages();
                    document.getElementById('sendBtn').disabled = false;
                }, 1000);
            });
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
        
        function exportData() {
            fetch('/export')
                .then(res => res.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `chat_data_${new Date().toISOString().split('T')[0]}.json`;
                    a.click();
                });
        }
        
        function clearChat() {
            if (confirm('🗑️ Are you sure you want to clear all messages?')) {
                fetch('/clear', {method: 'POST'})
                    .then(() => loadMessages());
            }
        }
        
        // Load messages on page load
        loadMessages();
        
        // Auto-refresh every 5 seconds
        setInterval(loadMessages, 5000);
    </script>
</body>
</html>
'''
