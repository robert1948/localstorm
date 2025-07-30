import axios from 'axios';
import { AIRequest, AIResponse } from '../../shared/types/ai.types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class AIService {
    async getAIResponse(request: AIRequest): Promise<AIResponse> {
        try {
            const response = await axios.post(`${API_URL}/ai`, request);
            return response.data;
        } catch (error) {
            throw new Error(`AI Service Error: ${error.response?.data?.message || error.message}`);
        }
    }

    async getAIModels(): Promise<string[]> {
        try {
            const response = await axios.get(`${API_URL}/ai/models`);
            return response.data;
        } catch (error) {
            throw new Error(`AI Models Retrieval Error: ${error.response?.data?.message || error.message}`);
        }
    }
}

export default new AIService();