import apiClient from './index';

// Define the interface for an Alert
export interface Alert {
  id?: number;
  student_id: number;
  student_name?: string;
  module_id: number;
  module_title?: string;
  week_number: number;
  reason: string;
  created_at: string;
  resolved: boolean;
  is_active?: boolean;
}

// API service functions
export const getAlerts = () => {
  return apiClient.get<Alert[]>('/admin/alerts');
};

export const getAlertsByStudentId = (studentId: number) => {
  return apiClient.get<Alert[]>(`/admin/alerts/student/${studentId}`);
};

export const addAlert = (alert: Omit<Alert, 'id' | 'student_name' | 'module_title' | 'created_at' | 'resolved' | 'is_active'>) => {
  return apiClient.post('/admin/alerts', alert);
};

export const resolveAlert = (id: number) => {
  return apiClient.put(`/admin/alerts/${id}/resolve`);
};

export const deleteAlert = (id: number) => {
  return apiClient.delete(`/admin/alerts/${id}`);
};
