import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

const apiService = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Interceptors for request and response
apiService.interceptors.request.use(
  (config) => {
    // Add any custom headers or configurations here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiService.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Example API calls
export const getExampleData = async () => {
  return await apiService.get('/example');
};

export const postExampleData = async (data) => {
  return await apiService.post('/example', data);
};

export default apiService;