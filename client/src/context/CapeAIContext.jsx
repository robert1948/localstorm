// client/src/context/CapeAIContext.jsx
import React, { createContext, useState, useCallback } from 'react';

export const CapeAIContext = createContext({
  isVisible: true,
  messages: [],
  toggleVisibility: () => {},
  addMessage: () => {},
});

export const CapeAIProvider = ({ children }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [messages, setMessages] = useState([
    { from: 'assistant', text: 'Hi! I’m CapeAI. How can I help you today?' },
  ]);

  const toggleVisibility = () => setIsVisible((prev) => !prev);

  const addMessage = useCallback((from, text) => {
    setMessages((prev) => [...prev, { from, text }]);
  }, []);

  return (
    <CapeAIContext.Provider
      value={{
        isVisible,
        messages,
        toggleVisibility,
        addMessage,
      }}
    >
      {children}
    </CapeAIContext.Provider>
  );
};
