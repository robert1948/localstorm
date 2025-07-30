export const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

export const validatePassword = (password: string): boolean => {
    return password.length >= 8; // Minimum length of 8 characters
};

export const validateUsername = (username: string): boolean => {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/; // Alphanumeric and underscores, 3-20 characters
    return usernameRegex.test(username);
};

export const validateProjectName = (projectName: string): boolean => {
    return projectName.length > 0 && projectName.length <= 100; // Non-empty and max length of 100
};

export const validateAIInput = (input: string): boolean => {
    return input.length > 0 && input.length <= 500; // Non-empty and max length of 500
};