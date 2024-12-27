<template>
  <v-container fluid>
    <v-card>
      <v-card-title class="d-flex align-center justify-space-between">
        Users Management
        <v-btn color="primary" @click="dialog.add = true">
          <v-icon start>mdi-plus</v-icon>
          Add User
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Search and Filters -->
        <v-row class="mb-4">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              label="Search Users"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              hide-details
              class="mb-2"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="4">
            <v-select
              v-model="roleFilter"
              :items="roles"
              label="Filter by Role"
              density="compact"
              hide-details
              class="mb-2"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="4">
            <v-select
              v-model="statusFilter"
              :items="['All', 'Active', 'Inactive']"
              label="Filter by Status"
              density="compact"
              hide-details
              class="mb-2"
            ></v-select>
          </v-col>
        </v-row>

        <!-- Users Table -->
        <v-data-table
          :headers="headers"
          :items="filteredUsers"
          :search="search"
          :loading="loading"
        >
          <!-- Status Column -->
          <template v-slot:item.status="{ item }">
            <v-chip
              :color="item.raw.status === 'Active' ? 'success' : 'error'"
              size="small"
            >
              {{ item.raw.status }}
            </v-chip>
          </template>

          <!-- Actions Column -->
          <template v-slot:item.actions="{ item }">
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="primary"
              class="mr-2"
              @click="editUser(item.raw)"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              @click="deleteUser(item.raw)"
            ></v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Add/Edit User Dialog -->
    <v-dialog v-model="dialog.add" max-width="600px">
      <v-card>
        <v-card-title>{{ editedUser.id ? 'Edit User' : 'Add New User' }}</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedUser.firstName"
                  label="First Name"
                  required
                  :rules="[v => !!v || 'First name is required']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedUser.lastName"
                  label="Last Name"
                  required
                  :rules="[v => !!v || 'Last name is required']"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedUser.email"
                  label="Email"
                  type="email"
                  required
                  :rules="emailRules"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedUser.role"
                  :items="roles"
                  label="Role"
                  required
                  :rules="[v => !!v || 'Role is required']"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedUser.status"
                  :items="['Active', 'Inactive']"
                  label="Status"
                  required
                ></v-select>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="dialog.add = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveUser" :loading="saving">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="dialog.delete" max-width="400px">
      <v-card>
        <v-card-title>Delete User</v-card-title>
        <v-card-text>
          Are you sure you want to delete this user? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="dialog.delete = false">Cancel</v-btn>
          <v-btn 
            color="error" 
            @click="confirmDelete"
            :loading="deleting"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Data
const search = ref('')
const roleFilter = ref('All')
const statusFilter = ref('All')
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const valid = ref(false)
const form = ref(null)

const dialog = ref({
  add: false,
  delete: false
})

const roles = ['All', 'admin', 'principal', 'hod', 'faculty', 'lab_assistant', 'student']

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Role', key: 'role' },
  { title: 'Status', key: 'status' },
  { title: 'Last Login', key: 'lastLogin' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const users = ref([])
const editedUser = ref({
  id: null,
  firstName: '',
  lastName: '',
  email: '',
  role: '',
  status: 'Active'
})
const userToDelete = ref(null)

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Email must be valid'
]

// Computed
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const roleMatch = roleFilter.value === 'All' || user.role === roleFilter.value
    const statusMatch = statusFilter.value === 'All' || user.status === statusFilter.value
    return roleMatch && statusMatch
  })
})

// Methods
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/admin/users')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
}

const editUser = (user) => {
  editedUser.value = { ...user }
  dialog.value.add = true
}

const deleteUser = (user) => {
  userToDelete.value = user
  dialog.value.delete = true
}

const saveUser = async () => {
  if (!form.value.validate()) return

  saving.value = true
  try {
    if (editedUser.value.id) {
      await axios.put(`/api/v1/admin/users/${editedUser.value.id}`, editedUser.value)
    } else {
      await axios.post('/api/v1/admin/users', editedUser.value)
    }
    await fetchUsers()
    dialog.value.add = false
  } catch (error) {
    console.error('Error saving user:', error)
  } finally {
    saving.value = false
  }
}

const confirmDelete = async () => {
  if (!userToDelete.value) return

  deleting.value = true
  try {
    await axios.delete(`/api/v1/admin/users/${userToDelete.value.id}`)
    await fetchUsers()
    dialog.value.delete = false
  } catch (error) {
    console.error('Error deleting user:', error)
  } finally {
    deleting.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchUsers()
})
</script>
