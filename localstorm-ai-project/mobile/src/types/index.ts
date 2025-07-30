// This file exports types and interfaces used throughout the mobile application.

export interface User {
    id: string;
    name: string;
    email: string;
    preferences: UserPreferences;
}

export interface UserPreferences {
    theme: string;
    notificationsEnabled: boolean;
    language: string;
}

export interface AIResponse {
    id: string;
    content: string;
    createdAt: Date;
}

export interface Conversation {
    id: string;
    userId: string;
    messages: Message[];
    createdAt: Date;
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

export interface AnalyticsData {
    userId: string;
    engagementScore: number;
    lastActive: Date;
}