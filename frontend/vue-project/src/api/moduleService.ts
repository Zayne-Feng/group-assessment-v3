import apiClient from './index';

export interface Module {
  id: number;
  module_code: string;
  module_title: string;
  credit: number;
  academic_year: string;
  is_active: boolean;
}

export const getModules = () => {
  return apiClient.get<Module[]>('/admin/modules');
};
