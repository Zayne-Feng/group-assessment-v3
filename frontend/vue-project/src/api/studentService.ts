import apiClient from './index';

// Define the interface for a Student
export interface Student {
  id?: number;
  student_number: string;
  full_name: string;
  email: string;
  course_name?: string;
  year_of_study?: number;
  is_active?: boolean;
  enrolments?: string[]; // Assuming enrolments are just module titles for display
}

// API service functions
export const getStudents = () => {
  return apiClient.get<Student[]>('/analysis/students');
};

export const getStudentById = (id: number) => {
  return apiClient.get<Student>(`/analysis/students/${id}`);
};

export const addStudent = (student: Omit<Student, 'id' | 'enrolments'>) => {
  return apiClient.post('/admin/students', student);
};

export const updateStudent = (id: number, student: Student) => {
  return apiClient.put(`/admin/students/${id}`, student);
};

export const deleteStudent = (id: number) => {
  return apiClient.delete(`/admin/students/${id}`);
};
