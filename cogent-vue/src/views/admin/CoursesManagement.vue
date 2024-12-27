<template>
  <div class="courses-management">
    <v-container>
      <!-- Header -->
      <v-row class="mb-4">
        <v-col cols="12" sm="8">
          <h2 class="text-h4">Courses Management</h2>
        </v-col>
        <v-col cols="12" sm="4" class="text-sm-right">
          <v-btn
            color="primary"
            @click="openAddDialog"
            prepend-icon="mdi-plus"
          >
            Add Course
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search and Filter -->
      <v-row class="mb-4">
        <v-col cols="12" sm="3">
          <v-text-field
            v-model="search"
            label="Search Courses"
            prepend-inner-icon="mdi-magnify"
            clearable
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="3">
          <v-select
            v-model="departmentFilter"
            :items="departments"
            item-title="name"
            item-value="id"
            label="Filter by Department"
            clearable
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" sm="3">
          <v-select
            v-model="semesterFilter"
            :items="[1,2,3,4,5,6,7,8]"
            label="Filter by Semester"
            clearable
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" sm="3">
          <v-select
            v-model="typeFilter"
            :items="courseTypes"
            label="Filter by Type"
            clearable
            hide-details
          ></v-select>
        </v-col>
      </v-row>

      <!-- Data Table -->
      <v-card>
        <v-data-table
          :headers="headers"
          :items="filteredCourses"
          :loading="loading"
          :search="search"
          class="elevation-1"
        >
          <!-- Custom Column Slots -->
          <template v-slot:item.type="{ item }">
            <v-chip
              :color="getTypeColor(item.raw.type)"
              size="small"
            >
              {{ item.raw.type }}
            </v-chip>
          </template>

          <template v-slot:item.status="{ item }">
            <v-chip
              :color="item.raw.is_active ? 'success' : 'error'"
              :text="item.raw.is_active ? 'Active' : 'Inactive'"
              size="small"
            ></v-chip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              variant="text"
              size="small"
              color="primary"
              @click="openEditDialog(item.raw)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              variant="text"
              size="small"
              :color="item.raw.is_active ? 'error' : 'success'"
              @click="toggleStatus(item.raw)"
            >
              <v-icon>{{ item.raw.is_active ? 'mdi-close' : 'mdi-check' }}</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
    </v-container>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditing ? 'Edit Course' : 'Add Course' }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid" @submit.prevent="saveCourse">
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.name"
                    label="Course Name*"
                    :rules="[v => !!v || 'Name is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.code"
                    label="Course Code*"
                    :rules="[v => !!v || 'Code is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="editedItem.department_id"
                    :items="departments"
                    item-title="name"
                    item-value="id"
                    label="Department*"
                    :rules="[v => !!v || 'Department is required']"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="editedItem.type"
                    :items="courseTypes"
                    label="Course Type*"
                    :rules="[v => !!v || 'Course type is required']"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.credits"
                    label="Credits*"
                    type="number"
                    min="1"
                    max="6"
                    :rules="[
                      v => !!v || 'Credits are required',
                      v => (v && v >= 1 && v <= 6) || 'Credits must be between 1 and 6'
                    ]"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="editedItem.semester"
                    :items="[1,2,3,4,5,6,7,8]"
                    label="Semester*"
                    :rules="[v => !!v || 'Semester is required']"
                    required
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            :loading="saving"
            :disabled="!valid || saving"
            @click="saveCourse"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="confirmDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirm Action</v-card-title>
        <v-card-text>
          {{ confirmMessage }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="confirmDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            :loading="saving"
            @click="confirmAction"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar for notifications -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'CoursesManagement',

  setup() {
    // Data
    const courses = ref([])
    const departments = ref([])
    const loading = ref(false)
    const dialog = ref(false)
    const confirmDialog = ref(false)
    const valid = ref(false)
    const saving = ref(false)
    const search = ref('')
    const departmentFilter = ref(null)
    const semesterFilter = ref(null)
    const typeFilter = ref(null)
    const form = ref(null)
    const isEditing = ref(false)
    const confirmAction = ref(null)
    const confirmMessage = ref('')
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    const courseTypes = ['theory', 'practical', 'project']

    const defaultItem = {
      name: '',
      code: '',
      credits: 3,
      type: 'theory',
      semester: 1,
      department_id: null,
      is_active: true
    }

    const editedItem = ref({ ...defaultItem })

    // Table headers
    const headers = [
      { title: 'Name', key: 'name', align: 'start', sortable: true },
      { title: 'Code', key: 'code', align: 'start', sortable: true },
      { title: 'Department', key: 'department.name', align: 'start', sortable: true },
      { title: 'Credits', key: 'credits', align: 'center', sortable: true },
      { title: 'Type', key: 'type', align: 'center', sortable: true },
      { title: 'Semester', key: 'semester', align: 'center', sortable: true },
      { title: 'Status', key: 'status', align: 'center', sortable: false },
      { title: 'Actions', key: 'actions', align: 'center', sortable: false }
    ]

    // Computed
    const filteredCourses = computed(() => {
      let filtered = [...courses.value]
      
      if (departmentFilter.value) {
        filtered = filtered.filter(course => course.department_id === departmentFilter.value)
      }
      
      if (semesterFilter.value) {
        filtered = filtered.filter(course => course.semester === semesterFilter.value)
      }
      
      if (typeFilter.value) {
        filtered = filtered.filter(course => course.type === typeFilter.value)
      }
      
      return filtered
    })

    // Methods
    const fetchDepartments = async () => {
      try {
        const response = await axios.get('/api/v1/colleges/departments/')
        departments.value = response.data
      } catch (error) {
        showError('Error fetching departments')
        console.error('Error:', error)
      }
    }

    const fetchCourses = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/v1/courses/')
        courses.value = response.data
      } catch (error) {
        showError('Error fetching courses')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const getTypeColor = (type) => {
      switch (type) {
        case 'theory':
          return 'primary'
        case 'practical':
          return 'success'
        case 'project':
          return 'warning'
        default:
          return 'grey'
      }
    }

    const openAddDialog = () => {
      isEditing.value = false
      editedItem.value = { ...defaultItem }
      dialog.value = true
    }

    const openEditDialog = (item) => {
      isEditing.value = true
      editedItem.value = { ...item }
      dialog.value = true
    }

    const closeDialog = () => {
      dialog.value = false
      editedItem.value = { ...defaultItem }
      form.value?.reset()
    }

    const saveCourse = async () => {
      if (!form.value?.validate()) return

      saving.value = true
      try {
        if (isEditing.value) {
          await axios.put(`/api/v1/courses/${editedItem.value.id}`, editedItem.value)
          showSuccess('Course updated successfully')
        } else {
          await axios.post('/api/v1/courses/', editedItem.value)
          showSuccess('Course added successfully')
        }
        await fetchCourses()
        closeDialog()
      } catch (error) {
        showError(error.response?.data?.detail || 'Error saving course')
        console.error('Error:', error)
      } finally {
        saving.value = false
      }
    }

    const toggleStatus = (item) => {
      confirmMessage.value = `Are you sure you want to ${item.is_active ? 'deactivate' : 'activate'} ${item.name}?`
      confirmAction.value = async () => {
        saving.value = true
        try {
          await axios.put(`/api/v1/courses/${item.id}`, {
            ...item,
            is_active: !item.is_active
          })
          await fetchCourses()
          showSuccess(`Course ${item.is_active ? 'deactivated' : 'activated'} successfully`)
        } catch (error) {
          showError('Error updating course status')
          console.error('Error:', error)
        } finally {
          saving.value = false
          confirmDialog.value = false
        }
      }
      confirmDialog.value = true
    }

    const showSuccess = (text) => {
      snackbar.value = {
        show: true,
        text,
        color: 'success'
      }
    }

    const showError = (text) => {
      snackbar.value = {
        show: true,
        text,
        color: 'error'
      }
    }

    // Lifecycle hooks
    onMounted(() => {
      fetchDepartments()
      fetchCourses()
    })

    return {
      // Data
      courses,
      departments,
      loading,
      dialog,
      confirmDialog,
      valid,
      saving,
      search,
      departmentFilter,
      semesterFilter,
      typeFilter,
      form,
      headers,
      editedItem,
      isEditing,
      confirmAction,
      confirmMessage,
      snackbar,
      courseTypes,
      filteredCourses,

      // Methods
      openAddDialog,
      openEditDialog,
      closeDialog,
      saveCourse,
      toggleStatus,
      getTypeColor
    }
  }
}
</script>

<style scoped>
.courses-management {
  padding: 20px;
}
</style>
