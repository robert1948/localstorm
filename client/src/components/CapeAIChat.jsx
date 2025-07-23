// client/src/components/CapeAIChat.jsx
import React, { useState, useRef, useEffect } from 'react';
import useCapeAI from '../hooks/useCapeAI';

export default function CapeAIChat() {
  // ✅ Always call ALL hooks at the top level unconditionally
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  
  // ✅ Hook call is now completely unconditional
  const capeAIData = useCapeAI();
  
  // ✅ useEffect must also be at the top level
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [capeAIData?.messages]);
  
  // Safe fallback if context is not available
  if (!capeAIData) {
    return null;
  }
  
  const { isVisible, messages, toggleVisibility, addMessage } = capeAIData;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    addMessage('user', inputMessage);
    const userMsg = inputMessage;
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const response = getAIResponse(userMsg);
      addMessage('assistant', response);
      setIsTyping(false);
    }, 1000);
  };

  const getAIResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    // Onboarding-focused responses
    if (message.includes('help') || message.includes('start')) {
      return "I'm here to help you get started! Let me guide you through the platform. Would you like to see your onboarding checklist or learn about specific features?";
    }
    if (message.includes('profile') || message.includes('account')) {
      return "Let's set up your profile! Click on your account settings to add your business information, preferences, and contact details.";
    }
    if (message.includes('agent') || message.includes('ai')) {
      return "Great question about AI agents! Our platform offers various AI tools for automation, content creation, and data analysis. Would you like me to show you how to access them?";
    }
    if (message.includes('dashboard')) {
      return "Your dashboard is your central hub! From there you can manage AI agents, view analytics, and access all platform features. Let me guide you through it.";
    }
    if (message.includes('pricing') || message.includes('cost')) {
      return "We offer flexible pricing options including pay-per-use and subscription models. Each AI agent has transparent pricing displayed. Would you like to see our pricing guide?";
    }
    
    return "I understand you're asking about: " + userMessage + ". Let me help you with that! Is there a specific part of the platform you'd like to explore?";
  };

  if (!isVisible) {
    return (
      <button
        onClick={toggleVisibility}
        className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
        aria-label="Open CapeAI Assistant"
      >
        🤖
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 h-[500px] bg-white border border-gray-200 rounded-lg shadow-xl flex flex-col z-50">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="text-xl">🤖</span>
          <div>
            <h3 className="font-semibold">CapeAI Assistant</h3>
            <p className="text-xs opacity-90">Your onboarding guide</p>
          </div>
        </div>
        <button
          onClick={toggleVisibility}
          className="text-white hover:text-gray-200 text-xl"
          aria-label="Close chat"
        >
          ×
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.from === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${
                message.from === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="text-sm">{message.text}</p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 p-3 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me anything about the platform..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
