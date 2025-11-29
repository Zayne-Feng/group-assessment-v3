import apiClient from './index';
import type { LoginCredentials, LoginResponse, RegisterCredentials, StudentRegisterCredentials } from '@/types/auth';

export const login = (credentials: LoginCredentials) => {
  return apiClient.post<LoginResponse>('/auth/login', credentials);
};

export const register = (credentials: RegisterCredentials) => {
  return apiClient.post('/auth/register', credentials);
};

export const registerStudent = (credentials: StudentRegisterCredentials) => {
  return apiClient.post('/auth/student/register', credentials);
};
