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
  collegeById: (id) => `/api/v1/dte-admin/colleges/${id}`,
  collegeDepartments: (id) => `/api/v1/dte-admin/colleges/${id}/departments`,
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

    async fetchDepartments() {
      this.loading = true
      try {
        // First ensure colleges are loaded
        if (this.colleges.length === 0) {
          await this.fetchColleges()
        }

        // Fetch departments for each college
        const departmentsPromises = this.colleges.map(college => 
          axios.get(API_ENDPOINTS.collegeDepartments(college.id))
        )

        const responses = await Promise.all(departmentsPromises)
        
        // Combine all departments and add college names
        this.departments = responses.flatMap(response => {
          const departments = Array.isArray(response.data) ? response.data : []
          return departments.map(dept => ({
            ...dept,
            college_name: this.colleges.find(c => c.id === dept.college_id)?.name || 'Unknown College'
          }))
        })

        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch departments'
        console.error('Error fetching departments:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createDepartment(departmentData) {
      this.loading = true
      try {
        const response = await axios.post(API_ENDPOINTS.collegeDepartments(departmentData.college_id), departmentData)
        const newDepartment = {
          ...response.data,
          college_name: this.colleges.find(c => c.id === response.data.college_id)?.name || 'Unknown College'
        }
        this.departments.push(newDepartment)
        this.error = null
        return newDepartment
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
        const response = await axios.put(API_ENDPOINTS.collegeDepartments(departmentData.college_id), departmentData)
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

    async deleteDepartment(departmentId, collegeId) {
      this.loading = true
      try {
        await axios.delete(`${API_ENDPOINTS.collegeDepartments(collegeId)}/${departmentId}`)
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
