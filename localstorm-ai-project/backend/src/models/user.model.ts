export class User {
    id: string;
    username: string;
    email: string;
    password: string;
    createdAt: Date;
    updatedAt: Date;

    constructor(id: string, username: string, email: string, password: string) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.password = password;
        this.createdAt = new Date();
        this.updatedAt = new Date();
    }

    // Method to update user information
    updateUserInfo(username?: string, email?: string, password?: string): void {
        if (username) this.username = username;
        if (email) this.email = email;
        if (password) this.password = password;
        this.updatedAt = new Date();
    }
}