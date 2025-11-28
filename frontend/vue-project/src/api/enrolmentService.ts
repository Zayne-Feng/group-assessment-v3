import apiClient from './index';

// Define the interface for an Enrolment
export interface Enrolment {
  id?: number;
  student_id: number;
  student_name?: string;
  module_id: number;
  module_title?: string;
  enrol_date: string;
}

// API service functions
export const getEnrolments = () => {
  return apiClient.get<Enrolment[]>('/admin/enrolments');
};

export const addEnrolment = (enrolment: Omit<Enrolment, 'id' | 'student_name' | 'module_title'>) => {
  return apiClient.post('/admin/enrolments', enrolment);
};

export const updateEnrolment = (id: number, enrolment: Enrolment) => {
  return apiClient.put(`/admin/enrolments/${id}`, enrolment);
};

export const deleteEnrolment = (id: number) => {
  return apiClient.delete(`/admin/enrolments/${id}`);
};
