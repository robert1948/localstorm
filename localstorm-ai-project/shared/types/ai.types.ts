// filepath: /localstorm-ai-project/localstorm-ai-project/shared/types/ai.types.ts
export interface AIModel {
    id: string;
    name: string;
    description: string;
    version: string;
    provider: string;
    capabilities: string[];
}

export interface AIRequest {
    modelId: string;
    input: string;
    parameters?: Record<string, any>;
}

export interface AIResponse {
    modelId: string;
    output: string;
    usage: {
        tokens: number;
        time: number; // in milliseconds
    };
}

export interface AIAnalytics {
    modelId: string;
    requestCount: number;
    successCount: number;
    failureCount: number;
    averageResponseTime: number; // in milliseconds
}