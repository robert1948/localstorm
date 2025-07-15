import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import { AuthProvider } from './context/AuthContext';
import { CapeAIProvider } from './context/CapeAIContext';
import './styles.css';

const rootElement = document.getElementById('root');

if (rootElement) {
  createRoot(rootElement).render(
    <BrowserRouter>
      <AuthProvider>
        <CapeAIProvider>
          <App />
        </CapeAIProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
