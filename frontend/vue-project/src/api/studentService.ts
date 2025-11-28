import apiClient from './index';

export interface Student {
  id?: number;
  student_number: string;
  full_name: string;
  email: string;
  course_name?: string;
  year_of_study?: number;
}

export const getStudents = () => {
  return apiClient.get<Student[]>('/analysis/students');
};

export const addStudent = (student: Omit<Student, 'id'>) => {
  return apiClient.post('/admin/students', student);
};

export const updateStudent = (id: number, student: Student) => {
  return apiClient.put(`/admin/students/${id}`, student);
};

export const deleteStudent = (id: number) => {
  return apiClient.delete(`/admin/students/${id}`);
};
