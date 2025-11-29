import apiClient from './index';

// Define the interface for a Survey Response
export interface SurveyResponse {
  id?: number;
  student_id: number;
  module_id: number;
  week_number: number;
  stress_level: number;
  hours_slept?: number;
  mood_comment?: string;
  student_name?: string; // Included for display purposes
  module_title?: string; // Included for display purposes
}

// API service functions
export const getSurveyResponses = () => {
  return apiClient.get<SurveyResponse[]>('/admin/survey-responses');
};

export const addSurveyResponse = (response: Omit<SurveyResponse, 'id' | 'student_name' | 'module_title'>) => {
  return apiClient.post('/admin/survey-responses', response);
};

export const updateSurveyResponse = (id: number, response: Partial<SurveyResponse>) => {
  return apiClient.put(`/admin/survey-responses/${id}`, response);
};

export const deleteSurveyResponse = (id: number) => {
  return apiClient.delete(`/admin/survey-responses/${id}`);
};
