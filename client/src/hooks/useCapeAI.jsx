import { useContext } from 'react';
import { CapeAIContext } from '../context/CapeAIContext';

export default function useCapeAI() {
  const context = useContext(CapeAIContext);
  
  if (!context) {
    throw new Error('useCapeAI must be used within a CapeAIProvider');
  }
  
  return context;
}
