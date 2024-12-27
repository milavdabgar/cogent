import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Remove /api/v1 from baseURL since we'll include it in the endpoints
axios.defaults.baseURL = API_URL

// API endpoints
const API_ENDPOINTS = {
  // DTE Admin endpoints
  stats: '/api/v1/dte-admin/stats',
  colleges: '/api/v1/dte-admin/colleges',
  collegeById: (id) => `/api/v1/dte-admin/colleges/${id}`
}

export const useDTEAdminStore = defineStore('dte-admin', {
  state: () => ({
    stats: null,
    colleges: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchStats() {
      this.loading = true
      try {
        const response = await axios.get(API_ENDPOINTS.stats)
        this.stats = response.data
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch stats'
        console.error('Error fetching DTE admin stats:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchColleges(params = {}) {
      this.loading = true
      try {
        const response = await axios.get(API_ENDPOINTS.colleges, { params })
        this.colleges = Array.isArray(response.data) ? response.data : []
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch colleges'
        console.error('Error fetching colleges:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createCollege(collegeData) {
      this.loading = true
      try {
        const response = await axios.post(API_ENDPOINTS.colleges, collegeData)
        this.colleges.push(response.data)
        this.error = null
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create college'
        console.error('Error creating college:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateCollege(collegeId, collegeData) {
      this.loading = true
      try {
        const response = await axios.put(API_ENDPOINTS.collegeById(collegeId), collegeData)
        const index = this.colleges.findIndex(c => c.id === collegeId)
        if (index !== -1) {
          this.colleges[index] = response.data
        }
        this.error = null
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update college'
        console.error('Error updating college:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteCollege(collegeId) {
      this.loading = true
      try {
        await axios.delete(API_ENDPOINTS.collegeById(collegeId))
        this.colleges = this.colleges.filter(c => c.id !== collegeId)
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete college'
        console.error('Error deleting college:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
