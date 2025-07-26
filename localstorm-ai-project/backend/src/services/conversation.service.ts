import { ConversationModel } from '../models/conversation.model';

export class ConversationService {
    private conversations: ConversationModel[];

    constructor() {
        this.conversations = [];
    }

    public createConversation(conversationData: Partial<ConversationModel>): ConversationModel {
        const newConversation = new ConversationModel(conversationData);
        this.conversations.push(newConversation);
        return newConversation;
    }

    public getConversationById(conversationId: string): ConversationModel | undefined {
        return this.conversations.find(conversation => conversation.id === conversationId);
    }

    public getAllConversations(): ConversationModel[] {
        return this.conversations;
    }

    public updateConversation(conversationId: string, updatedData: Partial<ConversationModel>): ConversationModel | undefined {
        const conversation = this.getConversationById(conversationId);
        if (conversation) {
            Object.assign(conversation, updatedData);
            return conversation;
        }
        return undefined;
    }

    public deleteConversation(conversationId: string): boolean {
        const index = this.conversations.findIndex(conversation => conversation.id === conversationId);
        if (index !== -1) {
            this.conversations.splice(index, 1);
            return true;
        }
        return false;
    }
}