import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

axios.defaults.baseURL = `${API_URL}/api/v1`

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
        const response = await axios.get('/dte-admin/stats')
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
        const response = await axios.get('/dte-admin/colleges', { params })
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
        const response = await axios.post('/dte-admin/colleges', collegeData)
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
        const response = await axios.put(`/dte-admin/colleges/${collegeId}`, collegeData)
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
        await axios.delete(`/dte-admin/colleges/${collegeId}`)
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
        const response = await axios.get('/dte-admin/departments', { params })
        this.departments = response.data.map(dept => ({
          ...dept,
          college_name: this.colleges.find(c => c.id === dept.college_id)?.name || ''
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
        const response = await axios.post('/dte-admin/departments', departmentData)
        this.departments.push(response.data)
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
        const response = await axios.put(`/dte-admin/departments/${departmentId}`, departmentData)
        const index = this.departments.findIndex(d => d.id === departmentId)
        if (index !== -1) {
          this.departments[index] = response.data
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
        await axios.delete(`/dte-admin/departments/${departmentId}`)
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
