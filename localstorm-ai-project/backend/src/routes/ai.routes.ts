import { Router } from 'express';
import { 
    getAIModels, 
    createAIModel, 
    updateAIModel, 
    deleteAIModel, 
    interactWithAI 
} from '../controllers/ai.controller';

const router = Router();

// Route to get all AI models
router.get('/models', getAIModels);

// Route to create a new AI model
router.post('/models', createAIModel);

// Route to update an existing AI model
router.put('/models/:id', updateAIModel);

// Route to delete an AI model
router.delete('/models/:id', deleteAIModel);

// Route to interact with an AI model
router.post('/interact', interactWithAI);

export default router;