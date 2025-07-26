// This file exports utility functions for various tasks.

export const formatDate = (date: Date): string => {
    return date.toISOString().split('T')[0];
};

export const capitalizeFirstLetter = (string: string): string => {
    return string.charAt(0).toUpperCase() + string.slice(1);
};

export const debounce = (func: Function, delay: number) => {
    let timeoutId: NodeJS.Timeout;
    return (...args: any[]) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func(...args);
        }, delay);
    };
};

export const isEmptyObject = (obj: object): boolean => {
    return Object.keys(obj).length === 0;
};

export const generateRandomId = (): string => {
    return Math.random().toString(36).substr(2, 9);
};