import apiClient from './index';

// Define the interface for a SurveyResponse
export interface SurveyResponse {
  id?: number;
  student_id: number | null;
  module_id: number | null;
  week_number: number | null;
  stress_level: number;
  hours_slept: number;
  mood_comment: string;
  created_at?: string;
  is_active?: boolean;
}

// API service functions
export const submitSurvey = (survey: SurveyResponse) => {
  return apiClient.post('/admin/survey-responses', survey);
};

// Potentially add other CRUD operations if needed for admin views
export const getSurveyResponses = () => {
  return apiClient.get<SurveyResponse[]>('/admin/survey-responses');
};

export const updateSurveyResponse = (id: number, survey: SurveyResponse) => {
  return apiClient.put(`/admin/survey-responses/${id}`, survey);
};

export const deleteSurveyResponse = (id: number) => {
  return apiClient.delete(`/admin/survey-responses/${id}`);
};
