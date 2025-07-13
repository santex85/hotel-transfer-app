// src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // URL нашего бэкенда
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to handle form data for login
apiClient.interceptors.request.use((config) => {
  // For login requests, set the correct content type
  if (config.url === '/api/v1/token') {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  return config;
});

export default apiClient; 