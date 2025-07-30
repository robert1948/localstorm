// filepath: /localstorm-ai-project/localstorm-ai-project/shared/types/api.types.ts
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    message?: string;
}

export interface ApiError {
    success: false;
    error: string;
}

export interface ApiRequest<T> {
    body: T;
    headers?: Record<string, string>;
    params?: Record<string, string>;
    query?: Record<string, string>;
}

export interface Pagination {
    page: number;
    limit: number;
    total: number;
}

export interface ApiListResponse<T> extends ApiResponse<T[]> {
    pagination: Pagination;
}