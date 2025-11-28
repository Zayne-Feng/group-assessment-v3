import apiClient from './index';

// Define the interface for a Grade
export interface Grade {
  id?: number;
  student_id: number;
  student_name?: string;
  module_id: number;
  module_title?: string;
  assessment_name: string;
  grade: number;
}

// API service functions
export const getGrades = () => {
  return apiClient.get<Grade[]>('/admin/grades');
};

export const addGrade = (grade: Omit<Grade, 'id' | 'student_name' | 'module_title'>) => {
  return apiClient.post('/admin/grades', grade);
};

export const updateGrade = (id: number, grade: Grade) => {
  return apiClient.put(`/admin/grades/${id}`, grade);
};

export const deleteGrade = (id: number) => {
  return apiClient.delete(`/admin/grades/${id}`);
};
