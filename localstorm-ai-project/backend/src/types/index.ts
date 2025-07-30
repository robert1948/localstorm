export interface User {
    id: string;
    username: string;
    email: string;
    passwordHash: string;
    createdAt: Date;
    updatedAt: Date;
}

export interface Conversation {
    id: string;
    userId: string;
    messages: Message[];
    createdAt: Date;
    updatedAt: Date;
}

export interface Message {
    id: string;
    conversationId: string;
    senderId: string;
    content: string;
    createdAt: Date;
}

export interface Project {
    id: string;
    name: string;
    description: string;
    createdAt: Date;
    updatedAt: Date;
}

export interface Preference {
    userId: string;
    preferences: Record<string, any>;
}

export interface Analytics {
    userId: string;
    engagementMetrics: EngagementMetrics;
}

export interface EngagementMetrics {
    sessionDuration: number;
    interactions: number;
    lastActive: Date;
}

export interface AIResponse {
    model: string;
    response: string;
    createdAt: Date;
}