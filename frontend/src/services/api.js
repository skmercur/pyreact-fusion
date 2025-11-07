/**
 * API Client Service
 * Handles all API calls to the backend
 */
import axios from 'axios'

// Use relative URL when served from same origin, otherwise use env or default
// This works for both development (Vite proxy) and production (same server)
const getApiBaseUrl = () => {
  // If VITE_API_BASE_URL is set, use it
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  
  // In production (served from same server), use relative URL
  // In development (Vite dev server), use localhost
  if (import.meta.env.PROD) {
    return '' // Relative URL - same origin
  }
  
  return 'http://localhost:8000' // Development default
}

const API_BASE_URL = getApiBaseUrl()

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API methods
export const api = {
  // Health check
  health: () => apiClient.get('/api/health'),

  // Authentication
  login: (username, password) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    return apiClient.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  register: (userData) => apiClient.post('/api/auth/register', userData),

  // User endpoints
  getCurrentUser: () => apiClient.get('/api/auth/me'),
  getUsers: (skip = 0, limit = 100) =>
    apiClient.get(`/api/users?skip=${skip}&limit=${limit}`),
}

export default apiClient

