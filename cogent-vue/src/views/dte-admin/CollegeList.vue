<template>
  <div class="college-list">
    <v-container>
      <v-row class="mb-4">
        <v-col cols="12" class="d-flex justify-space-between align-center">
          <h2>Colleges</h2>
          <v-btn color="primary" @click="showAddModal">
            Add College
          </v-btn>
        </v-col>
      </v-row>

      <v-card>
        <v-data-table
          :headers="headers"
          :items="colleges"
          :loading="loading"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              variant="text"
              size="small"
              color="primary"
              class="mr-2"
              @click="editCollege(item)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              variant="text"
              size="small"
              color="error"
              @click="deleteCollege(item.id)"
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
          <span class="text-h5">{{ isEditing ? 'Edit College' : 'Add College' }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="collegeForm.name"
                label="Name"
                :rules="[v => !!v || 'Name is required']"
                required
              ></v-text-field>

              <v-text-field
                v-model="collegeForm.code"
                label="Code"
                :rules="[v => !!v || 'Code is required']"
                required
              ></v-text-field>

              <v-textarea
                v-model="collegeForm.address"
                label="Address"
                :rules="[v => !!v || 'Address is required']"
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
            @click="saveCollege"
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
        <v-card-title class="text-h5">Delete College</v-card-title>
        <v-card-text>Are you sure you want to delete this college?</v-card-text>
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
import axios from 'axios'

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Code', key: 'code' },
  { title: 'Address', key: 'address' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const colleges = ref([])
const dialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const valid = ref(false)
const form = ref(null)
const deleteId = ref(null)

const collegeForm = ref({
  name: '',
  code: '',
  address: ''
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

onMounted(async () => {
  await fetchColleges()
})

const fetchColleges = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/dte-admin/colleges')
    colleges.value = response.data
  } catch (error) {
    showError('Error fetching colleges')
    console.error('Error fetching colleges:', error)
  } finally {
    loading.value = false
  }
}

const showAddModal = () => {
  isEditing.value = false
  editingId.value = null
  collegeForm.value = {
    name: '',
    code: '',
    address: ''
  }
  dialog.value = true
}

const editCollege = (item) => {
  isEditing.value = true
  editingId.value = item.id
  collegeForm.value = {
    name: item.name,
    code: item.code,
    address: item.address
  }
  dialog.value = true
}

const saveCollege = async () => {
  if (!form.value.validate()) return

  saving.value = true
  try {
    if (isEditing.value) {
      await axios.put(`/api/v1/dte-admin/colleges/${editingId.value}`, collegeForm.value)
      showSuccess('College updated successfully')
    } else {
      await axios.post('/api/v1/dte-admin/colleges', collegeForm.value)
      showSuccess('College created successfully')
    }
    await fetchColleges()
    dialog.value = false
  } catch (error) {
    showError(error.response?.data?.detail || 'Error saving college')
  } finally {
    saving.value = false
  }
}

const deleteCollege = (id) => {
  deleteId.value = id
  deleteDialog.value = true
}

const confirmDelete = async () => {
  deleting.value = true
  try {
    await axios.delete(`/api/v1/dte-admin/colleges/${deleteId.value}`)
    await fetchColleges()
    showSuccess('College deleted successfully')
    deleteDialog.value = false
  } catch (error) {
    showError(error.response?.data?.detail || 'Error deleting college')
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
.college-list {
  padding: 20px;
}
</style>
