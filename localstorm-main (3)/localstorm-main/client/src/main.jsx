import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles.css';

// Global error handler for React errors
window.addEventListener('error', (event) => {
  console.warn('Global error caught:', event.error);
  event.preventDefault();
});

// Minimal setup without context providers to eliminate errors
ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
