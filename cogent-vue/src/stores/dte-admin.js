import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Remove /api/v1 from baseURL since we'll include it in the endpoints
axios.defaults.baseURL = API_URL

// API endpoints
const API_ENDPOINTS = {
  stats: '/api/v1/dte-admin/stats',
  colleges: '/api/v1/dte-admin/colleges',
  departments: '/api/v1/dte-admin/departments'
}

export const useDTEAdminStore = defineStore('dte-admin', {
  state: () => ({
    stats: null,
    colleges: [],
    departments: [],
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
      } finally {
        this.loading = false
      }
    },

    async fetchColleges(params = {}) {
      this.loading = true
      try {
        const response = await axios.get(API_ENDPOINTS.colleges, { params })
        this.colleges = response.data
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch colleges'
        console.error('Error fetching colleges:', error)
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
        const response = await axios.put(`${API_ENDPOINTS.colleges}/${collegeId}`, collegeData)
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
        await axios.delete(`${API_ENDPOINTS.colleges}/${collegeId}`)
        this.colleges = this.colleges.filter(c => c.id !== collegeId)
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete college'
        console.error('Error deleting college:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchDepartments(params = {}) {
      this.loading = true
      try {
        // First ensure colleges are loaded
        if (this.colleges.length === 0) {
          await this.fetchColleges()
        }
        
        const response = await axios.get(API_ENDPOINTS.departments, { params })
        this.departments = response.data.map(dept => ({
          ...dept,
          college_name: this.colleges.find(c => c.id === dept.college_id)?.name || 'Unknown College'
        }))
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch departments'
        console.error('Error fetching departments:', error)
      } finally {
        this.loading = false
      }
    },

    async createDepartment(departmentData) {
      this.loading = true
      try {
        const response = await axios.post(API_ENDPOINTS.departments, departmentData)
        this.departments.push({
          ...response.data,
          college_name: this.colleges.find(c => c.id === response.data.college_id)?.name || 'Unknown College'
        })
        this.error = null
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create department'
        console.error('Error creating department:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateDepartment(departmentId, departmentData) {
      this.loading = true
      try {
        const response = await axios.put(`${API_ENDPOINTS.departments}/${departmentId}`, departmentData)
        const index = this.departments.findIndex(d => d.id === departmentId)
        if (index !== -1) {
          this.departments[index] = {
            ...response.data,
            college_name: this.colleges.find(c => c.id === response.data.college_id)?.name || 'Unknown College'
          }
        }
        this.error = null
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update department'
        console.error('Error updating department:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteDepartment(departmentId) {
      this.loading = true
      try {
        await axios.delete(`${API_ENDPOINTS.departments}/${departmentId}`)
        this.departments = this.departments.filter(d => d.id !== departmentId)
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete department'
        console.error('Error deleting department:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
