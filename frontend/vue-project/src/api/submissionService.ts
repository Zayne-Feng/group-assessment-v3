import apiClient from './index';

// Define the interface for a Submission Record
export interface SubmissionRecord {
  id?: number;
  student_id: number;
  student_name?: string;
  module_id: number;
  module_title?: string;
  assessment_name: string;
  due_date: string;
  submitted_date: string | null;
  is_submitted: boolean;
  is_late: boolean;
}

// API service functions
export const getSubmissionRecords = () => {
  return apiClient.get<SubmissionRecord[]>('/admin/submission-records');
};

export const addSubmissionRecord = (record: Omit<SubmissionRecord, 'id' | 'student_name' | 'module_title'>) => {
  return apiClient.post('/admin/submission-records', record);
};

export const updateSubmissionRecord = (id: number, record: SubmissionRecord) => {
  return apiClient.put(`/admin/submission-records/${id}`, record);
};

export const deleteSubmissionRecord = (id: number) => {
  return apiClient.delete(`/admin/submission-records/${id}`);
};
