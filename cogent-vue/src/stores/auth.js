import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    profile: null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.role,
    hasRole: (state) => (role) => state.role === role,
    hasAnyRole: (state) => (roles) => roles.includes(state.role),
    defaultRoute: (state) => {
      switch (state.role) {
        case 'DTE_ADMIN':
          return '/dashboard/dte-admin'
        case 'GTU_ADMIN':
          return '/dashboard/gtu-admin'
        case 'PRINCIPAL':
          return '/dashboard/principal'
        case 'HOD':
          return '/dashboard/hod'
        case 'FACULTY':
          return '/dashboard/faculty'
        case 'LAB_ASSISTANT':
          return '/dashboard/lab-assistant'
        case 'STUDENT':
          return '/dashboard/student'
        default:
          return '/login'
      }
    },
    fullName: (state) => state.profile ? `${state.profile.first_name} ${state.profile.last_name}` : ''
  },

  actions: {
    async login(credentials) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.post('/auth/login', credentials)
        
        if (response.data && response.data.access_token) {
          this.token = response.data.access_token
          this.role = credentials.role
          
          // Store in localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('role', this.role)
          
          // Set the token in the API instance immediately
          api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          
          // Fetch user profile after successful login
          await this.fetchProfile()
          
          return true
        } else {
          throw new Error('Invalid response from server')
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        console.error('Login error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async signup(userData) {
      try {
        this.loading = true
        this.error = null
        const response = await api.post('/auth/signup', userData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Signup failed'
        console.error('Signup error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchProfile() {
      try {
        this.loading = true
        this.error = null
        const response = await api.get('/auth/profile/me')
        this.profile = response.data
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch profile'
        if (err.response?.status !== 401) {
          console.error('Profile fetch error:', err)
        }
        throw this.error
      } finally {
        this.loading = false
      }
    },
    
    async updateProfile(profileData) {
      try {
        this.loading = true
        this.error = null
        
        // Prepare data based on role
        const updateData = { 
          first_name: profileData.first_name,
          last_name: profileData.last_name,
          email: profileData.email,
          phone_number: profileData.phone_number,
          date_of_birth: profileData.date_of_birth ? new Date(profileData.date_of_birth).toISOString().split('T')[0] : null
        }

        // Only include role-specific details if they exist in the profile
        if (this.profile?.role === 'student' && (profileData.enrollment_number || profileData.current_semester || profileData.department)) {
          updateData.student_details = {
            enrollment_number: profileData.enrollment_number,
            current_semester: profileData.current_semester,
            department: profileData.department
          }
        } else if (this.profile?.role === 'faculty' && profileData.faculty_details) {
          updateData.faculty_details = {
            department: profileData.faculty_details.department,
            qualification: profileData.faculty_details.qualification,
            specialization: profileData.faculty_details.specialization,
            date_of_joining: profileData.faculty_details.date_of_joining ? 
              new Date(profileData.faculty_details.date_of_joining).toISOString().split('T')[0] : null
          }
        } else if (this.profile?.role === 'hod' && profileData.hod_details) {
          updateData.hod_details = {
            department: profileData.hod_details.department,
            qualification: profileData.hod_details.qualification,
            experience_years: profileData.hod_details.experience_years,
            date_of_joining: profileData.hod_details.date_of_joining ? 
              new Date(profileData.hod_details.date_of_joining).toISOString().split('T')[0] : null
          }
        } else if (this.profile?.role === 'principal' && profileData.principal_details) {
          updateData.principal_details = {
            qualification: profileData.principal_details.qualification,
            experience_years: profileData.principal_details.experience_years,
            date_of_joining: profileData.principal_details.date_of_joining ? 
              new Date(profileData.principal_details.date_of_joining).toISOString().split('T')[0] : null
          }
        } else if (this.profile?.role === 'lab_assistant' && profileData.lab_assistant_details) {
          updateData.lab_assistant_details = {
            department: profileData.lab_assistant_details.department,
            lab_type: profileData.lab_assistant_details.lab_type,
            date_of_joining: profileData.lab_assistant_details.date_of_joining ? 
              new Date(profileData.lab_assistant_details.date_of_joining).toISOString().split('T')[0] : null
          }
        }

        const response = await api.put('/auth/profile/me', updateData)
        this.profile = response.data
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to update profile'
        console.error('Profile update error:', err)
        throw this.error
      } finally {
        this.loading = false
      }
    },

    async changePassword(passwordData) {
      try {
        this.loading = true
        this.error = null
        const response = await api.post('/auth/profile/change-password', passwordData)
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to change password'
        console.error('Password change error:', err)
        throw this.error
      } finally {
        this.loading = false
      }
    },

    async requestPasswordReset(email) {
      try {
        this.loading = true
        this.error = null
        const response = await api.post('/auth/profile/reset-password', { email })
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to request password reset'
        console.error('Password reset request error:', err)
        throw this.error
      } finally {
        this.loading = false
      }
    },

    async confirmPasswordReset(token, newPassword, confirmPassword) {
      try {
        this.loading = true
        this.error = null
        if (newPassword !== confirmPassword) {
          throw new Error('Passwords do not match')
        }
        const response = await api.post('/auth/profile/reset-password/confirm', {
          token,
          new_password: newPassword,
          confirm_password: confirmPassword
        })
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to reset password'
        console.error('Password reset error:', err)
        throw this.error
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      this.role = null
      this.profile = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      // Remove the token from the API instance
      delete api.defaults.headers.common['Authorization']
    }
  }
})
