import React, { useEffect, useState } from 'react';
import { useAI } from '../hooks/useAI';
import { ChatMessage } from '../components/chat/ChatMessage';
import { ChatInput } from '../components/chat/ChatInput';
import './Chat.css';

const Chat = () => {
    const { sendMessage, messages, fetchMessages } = useAI();
    const [input, setInput] = useState('');

    useEffect(() => {
        fetchMessages();
    }, [fetchMessages]);

    const handleSend = () => {
        if (input.trim()) {
            sendMessage(input);
            setInput('');
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <ChatMessage key={index} message={msg} />
                ))}
            </div>
            <ChatInput 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                onSend={handleSend} 
            />
        </div>
    );
};

export default Chat;