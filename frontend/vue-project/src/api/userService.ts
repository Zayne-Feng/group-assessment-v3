import apiClient from './index';

// Define the interface for a User
export interface User {
  id?: number;
  username: string;
  password?: string; // Password is only for creation, not typically returned or updated directly
  role: string;
  created_at: string;
  is_active: boolean;
}

// API service functions
export const getUsers = () => {
  return apiClient.get<User[]>('/admin/users');
};

export const addUser = (user: Omit<User, 'id' | 'created_at'>) => {
  return apiClient.post('/admin/users', user);
};

export const updateUser = (id: number, user: Partial<Omit<User, 'password' | 'created_at'>>) => {
  return apiClient.put(`/admin/users/${id}`, user);
};

export const deleteUser = (id: number) => {
  return apiClient.delete(`/admin/users/${id}`);
};

export const resetUserPassword = (id: number, new_password: string) => {
  return apiClient.put(`/admin/users/${id}/reset-password`, { new_password });
};
