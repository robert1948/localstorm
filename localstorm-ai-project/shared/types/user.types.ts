// filepath: /localstorm-ai-project/localstorm-ai-project/shared/types/user.types.ts
export interface User {
    id: string;
    username: string;
    email: string;
    passwordHash: string;
    createdAt: Date;
    updatedAt: Date;
    preferences?: UserPreferences;
}

export interface UserPreferences {
    theme: string;
    notificationsEnabled: boolean;
    language: string;
    [key: string]: any; // Allows for additional dynamic preferences
}