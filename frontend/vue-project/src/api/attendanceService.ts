import apiClient from './index';

// Define the interface for an AttendanceRecord
export interface AttendanceRecord {
  id?: number;
  student_id: number;
  student_name?: string;
  module_id: number;
  module_title?: string;
  week_number: number;
  attended_sessions: number;
  total_sessions: number;
  attendance_rate: number; // This might be calculated on backend or frontend
}

// API service functions
export const getAttendanceRecords = () => {
  return apiClient.get<AttendanceRecord[]>('/admin/attendance-records');
};

export const addAttendanceRecord = (record: Omit<AttendanceRecord, 'id' | 'student_name' | 'module_title' | 'attendance_rate'>) => {
  return apiClient.post('/admin/attendance-records', record);
};

export const updateAttendanceRecord = (id: number, record: AttendanceRecord) => {
  return apiClient.put(`/admin/attendance-records/${id}`, record);
};

export const deleteAttendanceRecord = (id: number) => {
  return apiClient.delete(`/admin/attendance-records/${id}`);
};
