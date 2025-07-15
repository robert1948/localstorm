import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// Test with AuthContext only
function TestApp() {
  return (
    <div className="p-4">
      <h1>Test with AuthContext Added</h1>
      <p>Testing if AuthContext is the source of React error #321</p>
    </div>
  );
}

const rootElement = document.getElementById('root');

if (rootElement) {
  createRoot(rootElement).render(
    <React.StrictMode>
      <BrowserRouter>
        <AuthProvider>
          <TestApp />
        </AuthProvider>
      </BrowserRouter>
    </React.StrictMode>
  );
}
