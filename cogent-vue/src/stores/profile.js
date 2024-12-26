import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

const API_URL = 'http://localhost:8000'

// Create axios instance with base URL and interceptors
const api = axios.create({
  baseURL: `${API_URL}/api/v1`
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

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  async function fetchProfile() {
    try {
      loading.value = true
      error.value = null
      const response = await api.get('/profile/me')
      profile.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch profile'
      if (err.response?.status !== 401) {
        console.error('Profile fetch error:', err)
      }
      throw error.value
    } finally {
      loading.value = false
    }
  }
  
  async function updateProfile(profileData) {
    try {
      loading.value = true
      error.value = null
      
      // Prepare data based on role
      const updateData = { 
        first_name: profileData.first_name,
        last_name: profileData.last_name,
        email: profileData.email,
        phone_number: profileData.phone_number,
        date_of_birth: profileData.date_of_birth
      }

      // Only include role-specific details if they exist in the profile
      if (profile.value?.role === 'student' && (profileData.enrollment_number || profileData.current_semester || profileData.department)) {
        updateData.student_details = {
          enrollment_number: profileData.enrollment_number,
          current_semester: profileData.current_semester,
          department: profileData.department
        }
      } else if (profile.value?.role === 'faculty' && (profileData.department || profileData.qualification || profileData.specialization)) {
        updateData.faculty_details = {
          department: profileData.department,
          qualification: profileData.qualification,
          specialization: profileData.specialization
        }
      }

      const response = await api.put('/profile/me', updateData)
      profile.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update profile'
      console.error('Profile update error:', err)
      throw error.value
    } finally {
      loading.value = false
    }
  }
  
  async function changePassword(passwordData) {
    try {
      loading.value = true
      error.value = null
      await api.post('/profile/change-password', passwordData)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to change password'
      console.error('Password change error:', err)
      throw error.value
    } finally {
      loading.value = false
    }
  }
  
  async function requestPasswordReset(email) {
    try {
      loading.value = true
      error.value = null
      await api.post('/profile/reset-password', { email })
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to request password reset'
      console.error('Password reset request error:', err)
      throw error.value
    } finally {
      loading.value = false
    }
  }
  
  async function confirmPasswordReset(token, newPassword, confirmPassword) {
    try {
      loading.value = true
      error.value = null
      await api.post('/profile/reset-password-confirm', {
        token,
        new_password: newPassword,
        confirm_password: confirmPassword
      })
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to reset password'
      console.error('Password reset confirmation error:', err)
      throw error.value
    } finally {
      loading.value = false
    }
  }
  
  return {
    profile,
    loading,
    error,
    fetchProfile,
    updateProfile,
    changePassword,
    requestPasswordReset,
    confirmPasswordReset
  }
})
