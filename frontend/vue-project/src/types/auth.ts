export interface LoginCredentials {
  username: string;
  password: string;
  context: 'staff' | 'student';
}

export interface RegisterCredentials {
  username: string;
  password: string;
}

export interface StudentRegisterCredentials extends RegisterCredentials {
  student_number: string;
  full_name: string;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  message: string;
  user_role: string;
}
