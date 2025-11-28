import apiClient from './index';
import type { LoginCredentials, LoginResponse, RegisterCredentials } from '@/types/auth';

export const login = (credentials: LoginCredentials) => {
  return apiClient.post<LoginResponse>('/auth/login', credentials);
};

export const register = (credentials: RegisterCredentials) => {
  return apiClient.post('/auth/register', credentials);
};
