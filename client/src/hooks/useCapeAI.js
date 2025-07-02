// client/src/hooks/useCapeAI.js
import { useContext } from 'react';
import { CapeAIContext } from '../context/CapeAIContext';

const useCapeAI = () => useContext(CapeAIContext);
export default useCapeAI;
