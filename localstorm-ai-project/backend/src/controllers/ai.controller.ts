import { Request, Response } from 'express';
import { AIService } from '../services/ai.service';

const aiService = new AIService();

export const getAIResponse = async (req: Request, res: Response) => {
    try {
        const { prompt } = req.body;
        const response = await aiService.getResponse(prompt);
        res.status(200).json({ response });
    } catch (error) {
        res.status(500).json({ error: 'An error occurred while processing your request.' });
    }
};

export const trainAIModel = async (req: Request, res: Response) => {
    try {
        const { trainingData } = req.body;
        await aiService.trainModel(trainingData);
        res.status(200).json({ message: 'AI model training initiated.' });
    } catch (error) {
        res.status(500).json({ error: 'An error occurred while training the AI model.' });
    }
};

export const getModelStatus = async (req: Request, res: Response) => {
    try {
        const status = await aiService.getModelStatus();
        res.status(200).json({ status });
    } catch (error) {
        res.status(500).json({ error: 'An error occurred while retrieving model status.' });
    }
};