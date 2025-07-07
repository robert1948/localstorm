import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import { AuthProvider } from './context/AuthContext'; // ✅ Import the provider
import './styles.css';

const rootElement = document.getElementById('root');

if (rootElement) {
  createRoot(rootElement).render(
    <React.StrictMode>
      <BrowserRouter>
        <AuthProvider> {/* ✅ Context must wrap everything */}
          <App />
        </AuthProvider>
      </BrowserRouter>
    </React.StrictMode>
  );
}
