import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api'; // Update with your backend API URL

const apiService = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // Set a timeout for requests
});

// Interceptors for request and response
apiService.interceptors.request.use(
  (config) => {
    // Add any custom headers or authentication tokens here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiService.interceptors.response.use(
  (response) => {
    return response.data; // Return only the data from the response
  },
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Example API methods
export const fetchUserData = async (userId) => {
  return await apiService.get(`/users/${userId}`);
};

export const fetchAIModels = async () => {
  return await apiService.get('/ai/models');
};

export const createConversation = async (data) => {
  return await apiService.post('/conversations', data);
};

export const fetchAnalyticsData = async () => {
  return await apiService.get('/analytics');
};

export default apiService;