export interface User {
  id: string
  email: string
  username?: string
  full_name?: string
  is_active: boolean
  is_verified: boolean
  is_superuser: boolean
  organization_id?: string
  last_login_at?: string
  created_at: string
  updated_at: string
}

export interface Organization {
  id: string
  name: string
  slug: string
  is_active: boolean
  settings?: Record<string, any>
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  token: string
  user: User
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}
