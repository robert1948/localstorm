import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class AuthService {
    async login(username, password) {
        const response = await axios.post(`${API_URL}/auth/login`, { username, password });
        if (response.data.token) {
            localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
    }

    async logout() {
        localStorage.removeItem('user');
    }

    async register(username, email, password) {
        const response = await axios.post(`${API_URL}/auth/register`, { username, email, password });
        return response.data;
    }

    getCurrentUser() {
        return JSON.parse(localStorage.getItem('user'));
    }
}

export default new AuthService();