import { Router } from 'express';
import { createConversation, getConversations, getConversationById, updateConversation, deleteConversation } from '../controllers/conversation.controller';

const router = Router();

// Route to create a new conversation
router.post('/', createConversation);

// Route to get all conversations
router.get('/', getConversations);

// Route to get a conversation by ID
router.get('/:id', getConversationById);

// Route to update a conversation by ID
router.put('/:id', updateConversation);

// Route to delete a conversation by ID
router.delete('/:id', deleteConversation);

export default router;