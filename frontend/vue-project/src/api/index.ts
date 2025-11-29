import axios from 'axios';
import { useAuthStore } from '@/stores/auth'; // Import the auth store

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in headers
apiClient.interceptors.request.use(config => {
  // Get the auth store instance
  const authStore = useAuthStore();
  // Retrieve the token directly from the store's state
  const token = authStore.accessToken;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default apiClient;
