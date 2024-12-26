import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

// Create axios instance with base URL and interceptors
const api = axios.create({
  baseURL: API_URL
})

// Add request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.role,
    fullName: (state) => state.user ? `${state.user.first_name} ${state.user.last_name}` : '',
    defaultRoute: (state) => state.role ? `/dashboard/${state.role}` : '/'
  },

  actions: {
    async login(credentials) {
      try {
        // Create FormData object
        const formData = new FormData()
        formData.append('email', credentials.email)
        formData.append('password', credentials.password)
        if (credentials.role) {
          formData.append('role', credentials.role)
        }
        
        const response = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (response.data && response.data.access_token) {
          this.token = response.data.access_token
          this.role = credentials.role
          
          // Store in localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('role', this.role)
          
          // Fetch user profile after successful login
          await this.fetchProfile()
          
          return true
        } else {
          throw new Error('Invalid response from server')
        }
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    async signup(userData) {
      try {
        const response = await api.post('/auth/signup', userData)
        return response.data
      } catch (error) {
        console.error('Signup error:', error)
        throw error
      }
    },

    async fetchProfile() {
      try {
        const response = await api.get('/profile/me')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return response.data
      } catch (error) {
        console.error('Failed to fetch profile:', error)
        throw error
      }
    },

    async updateProfile(profileData) {
      try {
        const response = await api.put('/profile/me', profileData)
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return response.data
      } catch (error) {
        console.error('Failed to update profile:', error)
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.role = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      localStorage.removeItem('role')
    }
  }
})
