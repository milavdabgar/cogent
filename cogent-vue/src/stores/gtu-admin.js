import { defineStore } from 'pinia'
import { api } from '@/api'

export const useGTUAdminStore = defineStore('gtuAdmin', {
  state: () => ({
    departments: [],
    degreeLevels: [],
    degreePrograms: [],
    subjects: [],
    loading: false,
    error: null,
  }),

  actions: {
    // Departments
    async fetchDepartments() {
      try {
        this.loading = true
        const response = await api.get('/api/v1/gtu-admin/departments')
        this.departments = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error fetching departments'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createDepartment(data) {
      try {
        this.loading = true
        const response = await api.post('/api/v1/gtu-admin/departments', data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error creating department'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateDepartment(id, data) {
      try {
        this.loading = true
        const response = await api.put(`/api/v1/gtu-admin/departments/${id}`, data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error updating department'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteDepartment(id) {
      try {
        this.loading = true
        const response = await api.delete(`/api/v1/gtu-admin/departments/${id}`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error deleting department'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Degree Levels
    async fetchDegreeLevels() {
      try {
        this.loading = true
        const response = await api.get('/api/v1/gtu-admin/degree-levels')
        this.degreeLevels = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error fetching degree levels'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createDegreeLevel(data) {
      try {
        this.loading = true
        const response = await api.post('/api/v1/gtu-admin/degree-levels', data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error creating degree level'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateDegreeLevel(id, data) {
      try {
        this.loading = true
        const response = await api.put(`/api/v1/gtu-admin/degree-levels/${id}`, data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error updating degree level'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteDegreeLevel(id) {
      try {
        this.loading = true
        const response = await api.delete(`/api/v1/gtu-admin/degree-levels/${id}`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error deleting degree level'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Degree Programs
    async fetchDegreePrograms() {
      try {
        this.loading = true
        const response = await api.get('/api/v1/gtu-admin/degree-programs')
        this.degreePrograms = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error fetching degree programs'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createDegreeProgram(data) {
      try {
        this.loading = true
        const response = await api.post('/api/v1/gtu-admin/degree-programs', data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error creating degree program'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateDegreeProgram(id, data) {
      try {
        this.loading = true
        const response = await api.put(`/api/v1/gtu-admin/degree-programs/${id}`, data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error updating degree program'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteDegreeProgram(id) {
      try {
        this.loading = true
        const response = await api.delete(`/api/v1/gtu-admin/degree-programs/${id}`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error deleting degree program'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getProgramSubjects(programId) {
      try {
        this.loading = true
        const response = await api.get(`/api/v1/gtu-admin/degree-programs/${programId}/subjects`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error fetching program subjects'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Subjects
    async fetchSubjects() {
      try {
        this.loading = true
        const response = await api.get('/api/v1/gtu-admin/subjects')
        this.subjects = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error fetching subjects'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createSubject(data) {
      try {
        this.loading = true
        const response = await api.post('/api/v1/gtu-admin/subjects', data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error creating subject'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateSubject(id, data) {
      try {
        this.loading = true
        const response = await api.put(`/api/v1/gtu-admin/subjects/${id}`, data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error updating subject'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteSubject(id) {
      try {
        this.loading = true
        const response = await api.delete(`/api/v1/gtu-admin/subjects/${id}`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error deleting subject'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Program Subjects
    async mapSubjectToProgram(data) {
      try {
        this.loading = true
        const response = await api.post('/api/v1/gtu-admin/program-subjects', data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error mapping subject to program'
        throw error
      } finally {
        this.loading = false
      }
    },

    async unmapSubjectFromProgram(programId, subjectId) {
      try {
        this.loading = true
        const response = await api.delete(`/api/v1/gtu-admin/program-subjects/${programId}/${subjectId}`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error removing subject from program'
        throw error
      } finally {
        this.loading = false
      }
    },
  },
})
