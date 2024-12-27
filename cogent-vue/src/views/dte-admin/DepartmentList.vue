<template>
  <div class="department-list">
    <v-container>
      <v-row class="mb-4">
        <v-col cols="12" class="d-flex justify-space-between align-center">
          <h2>Departments</h2>
          <v-btn color="primary" @click="showAddModal">
            ADD DEPARTMENT
          </v-btn>
        </v-col>
      </v-row>

      <v-card>
        <v-data-table
          :headers="headers"
          :items="dteAdminStore.departments"
          :loading="dteAdminStore.loading"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              variant="text"
              size="small"
              color="primary"
              class="mr-2"
              @click="editDepartment(item)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              variant="text"
              size="small"
              color="error"
              @click="deleteDepartment(item.id)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
    </v-container>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditing ? 'Edit Department' : 'Add Department' }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="departmentForm.name"
                label="Name"
                :rules="[v => !!v || 'Name is required']"
                required
              ></v-text-field>

              <v-text-field
                v-model="departmentForm.code"
                label="Code"
                :rules="[v => !!v || 'Code is required']"
                required
              ></v-text-field>

              <v-select
                v-model="departmentForm.college_id"
                :items="dteAdminStore.colleges"
                item-title="name"
                item-value="id"
                label="College"
                :rules="[v => !!v || 'College is required']"
                required
              ></v-select>

              <v-textarea
                v-model="departmentForm.description"
                label="Description"
                :rules="[v => !!v || 'Description is required']"
                required
              ></v-textarea>
            </v-form>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="saveDepartment"
            :disabled="!valid"
            :loading="saving"
          >
            Save
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="dialog = false"
          >
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Delete Department</v-card-title>
        <v-card-text>Are you sure you want to delete this department?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="confirmDelete"
            :loading="deleting"
          >
            Yes
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="deleteDialog = false"
          >
            No
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

<script setup>
import { ref, onMounted } from 'vue'
import { useDTEAdminStore } from '@/stores/dte-admin'

const dteAdminStore = useDTEAdminStore()

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Code', key: 'code' },
  { title: 'College', key: 'college_name' },
  { title: 'Description', key: 'description' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const dialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const saving = ref(false)
const deleting = ref(false)
const valid = ref(false)
const form = ref(null)
const deleteId = ref(null)

const departmentForm = ref({
  name: '',
  code: '',
  college_id: '',
  description: ''
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

onMounted(async () => {
  try {
    // First fetch colleges
    await dteAdminStore.fetchColleges()
    // Then fetch departments
    await dteAdminStore.fetchDepartments()
  } catch (error) {
    showError(error.response?.data?.detail || 'Failed to load data')
  }
})

const showAddModal = () => {
  isEditing.value = false
  editingId.value = null
  departmentForm.value = {
    name: '',
    code: '',
    college_id: '',
    description: ''
  }
  dialog.value = true
}

const editDepartment = (item) => {
  isEditing.value = true
  editingId.value = item.id
  departmentForm.value = {
    name: item.name,
    code: item.code,
    college_id: item.college_id,
    description: item.description
  }
  dialog.value = true
}

const saveDepartment = async () => {
  if (!valid.value) return

  saving.value = true
  try {
    if (isEditing.value) {
      await dteAdminStore.updateDepartment(editingId.value, departmentForm.value)
      showSuccess('Department updated successfully')
    } else {
      await dteAdminStore.createDepartment(departmentForm.value)
      showSuccess('Department created successfully')
    }
    dialog.value = false
    await dteAdminStore.fetchDepartments()
  } catch (error) {
    showError(error.response?.data?.detail || 'Error saving department')
  } finally {
    saving.value = false
  }
}

const deleteDepartment = (id) => {
  deleteId.value = id
  deleteDialog.value = true
}

const confirmDelete = async () => {
  deleting.value = true
  try {
    await dteAdminStore.deleteDepartment(deleteId.value)
    showSuccess('Department deleted successfully')
    deleteDialog.value = false
  } catch (error) {
    showError(error.response?.data?.detail || 'Error deleting department')
  } finally {
    deleting.value = false
  }
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
</script>

<style scoped>
.department-list {
  padding: 20px;
}
</style>
