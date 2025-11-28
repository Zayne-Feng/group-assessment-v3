import apiClient from './index';

// Define interfaces for the data structures
export interface DashboardSummary {
  total_students: number;
  total_modules: number;
  pending_alerts_count: number;
  total_users: number;
}

export interface GradeDistribution {
  labels: string[];
  data: number[];
}

export interface StressGradeCorrelation {
  labels: string[];
  data: { x: number; y: number; name: string }[];
}

export interface TrendData {
  labels: string[];
  data: number[];
}

// API service functions
export const getDashboardSummary = () => {
  return apiClient.get<DashboardSummary>('/analysis/dashboard-summary');
};

export const getGradeDistribution = () => {
  return apiClient.get<GradeDistribution>('/analysis/grade-distribution');
};

export const getStressGradeCorrelation = () => {
  return apiClient.get<StressGradeCorrelation>('/analysis/stress-grade-correlation');
};

export const getStressTrendForStudent = (studentId: number) => {
  return apiClient.get<TrendData>(`/analysis/students/${studentId}/stress-trend`);
};

export const getAttendanceTrendForStudent = (studentId: number) => {
  return apiClient.get<TrendData>(`/analysis/students/${studentId}/attendance-trend`);
};
