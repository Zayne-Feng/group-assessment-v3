import apiClient from './index';

export interface Module {
  id?: number; // Make id optional for new modules
  module_code: string;
  module_title: string;
  credit: number;
  academic_year: string;
  is_active?: boolean; // Make is_active optional for new modules
}

export const getModules = () => {
  return apiClient.get<Module[]>('/admin/modules');
};

export const addModule = (moduleData: Omit<Module, 'id' | 'is_active'>) => {
  return apiClient.post<Module>('/admin/modules', moduleData);
};

export const updateModule = (id: number, moduleData: Partial<Module>) => {
  return apiClient.put<Module>(`/admin/modules/${id}`, moduleData);
};

export const deleteModule = (id: number) => {
  return apiClient.delete(`/admin/modules/${id}`);
};
