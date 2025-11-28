export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials extends LoginCredentials {
  // Potentially add other fields like email if needed in the future
}

export interface LoginResponse {
  access_token: string;
  message: string;
  user_role: string;
}
