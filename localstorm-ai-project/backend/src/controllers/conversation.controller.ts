import { Request, Response } from 'express';
import ConversationService from '../services/conversation.service';

class ConversationController {
    private conversationService: ConversationService;

    constructor() {
        this.conversationService = new ConversationService();
    }

    public async createConversation(req: Request, res: Response): Promise<Response> {
        try {
            const conversationData = req.body;
            const newConversation = await this.conversationService.createConversation(conversationData);
            return res.status(201).json(newConversation);
        } catch (error) {
            return res.status(500).json({ message: 'Error creating conversation', error });
        }
    }

    public async getConversation(req: Request, res: Response): Promise<Response> {
        try {
            const { id } = req.params;
            const conversation = await this.conversationService.getConversationById(id);
            if (!conversation) {
                return res.status(404).json({ message: 'Conversation not found' });
            }
            return res.status(200).json(conversation);
        } catch (error) {
            return res.status(500).json({ message: 'Error retrieving conversation', error });
        }
    }

    public async getAllConversations(req: Request, res: Response): Promise<Response> {
        try {
            const conversations = await this.conversationService.getAllConversations();
            return res.status(200).json(conversations);
        } catch (error) {
            return res.status(500).json({ message: 'Error retrieving conversations', error });
        }
    }
}

export default new ConversationController();