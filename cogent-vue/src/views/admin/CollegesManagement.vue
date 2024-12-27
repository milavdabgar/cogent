<template>
  <div class="colleges-management">
    <v-container>
      <!-- Header -->
      <v-row class="mb-4">
        <v-col cols="12" sm="8">
          <h2 class="text-h4">Colleges Management</h2>
        </v-col>
        <v-col cols="12" sm="4" class="text-sm-right">
          <v-btn
            color="primary"
            @click="openAddDialog"
            prepend-icon="mdi-plus"
          >
            Add College
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search and Filter -->
      <v-row class="mb-4">
        <v-col cols="12" sm="4">
          <v-text-field
            v-model="search"
            label="Search Colleges"
            prepend-inner-icon="mdi-magnify"
            clearable
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="stateFilter"
            :items="states"
            label="Filter by State"
            clearable
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="statusFilter"
            :items="[
              { title: 'Active', value: true },
              { title: 'Inactive', value: false }
            ]"
            label="Filter by Status"
            clearable
            hide-details
          ></v-select>
        </v-col>
      </v-row>

      <!-- Data Table -->
      <v-card>
        <v-data-table
          :headers="headers"
          :items="filteredColleges"
          :loading="loading"
          :search="search"
          class="elevation-1"
        >
          <!-- Custom Column Slots -->
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
          <span class="text-h5">{{ isEditing ? 'Edit College' : 'Add College' }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid" @submit.prevent="saveCollege">
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.name"
                    label="College Name*"
                    :rules="[v => !!v || 'Name is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.code"
                    label="College Code*"
                    :rules="[v => !!v || 'Code is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.address"
                    label="Address*"
                    :rules="[v => !!v || 'Address is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.city"
                    label="City*"
                    :rules="[v => !!v || 'City is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.state"
                    label="State*"
                    :rules="[v => !!v || 'State is required']"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.phone"
                    label="Phone"
                    type="tel"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.email"
                    label="Email"
                    type="email"
                    :rules="emailRules"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.website"
                    label="Website"
                    type="url"
                  ></v-text-field>
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
            @click="saveCollege"
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
  name: 'CollegesManagement',

  setup() {
    // Data
    const colleges = ref([])
    const loading = ref(false)
    const dialog = ref(false)
    const confirmDialog = ref(false)
    const valid = ref(false)
    const saving = ref(false)
    const search = ref('')
    const stateFilter = ref(null)
    const statusFilter = ref(null)
    const form = ref(null)
    const states = ref([])
    const isEditing = ref(false)
    const confirmAction = ref(null)
    const confirmMessage = ref('')
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    const defaultItem = {
      name: '',
      code: '',
      address: '',
      city: '',
      state: '',
      country: 'India',
      phone: '',
      email: '',
      website: '',
      is_active: true
    }

    const editedItem = ref({ ...defaultItem })

    // Table headers
    const headers = [
      { title: 'Name', key: 'name', align: 'start', sortable: true },
      { title: 'Code', key: 'code', align: 'start', sortable: true },
      { title: 'City', key: 'city', align: 'start', sortable: true },
      { title: 'State', key: 'state', align: 'start', sortable: true },
      { title: 'Phone', key: 'phone', align: 'start', sortable: true },
      { title: 'Status', key: 'status', align: 'center', sortable: false },
      { title: 'Actions', key: 'actions', align: 'center', sortable: false }
    ]

    // Form validation rules
    const emailRules = [
      v => !v || /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ]

    // Computed
    const filteredColleges = computed(() => {
      let filtered = [...colleges.value]
      
      if (stateFilter.value) {
        filtered = filtered.filter(college => college.state === stateFilter.value)
      }
      
      if (statusFilter.value !== null) {
        filtered = filtered.filter(college => college.is_active === statusFilter.value)
      }
      
      return filtered
    })

    // Methods
    const fetchColleges = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/v1/colleges/')
        colleges.value = response.data
        // Extract unique states for filter
        states.value = [...new Set(colleges.value.map(college => college.state))].sort()
      } catch (error) {
        showError('Error fetching colleges')
        console.error('Error:', error)
      } finally {
        loading.value = false
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

    const saveCollege = async () => {
      if (!form.value?.validate()) return

      saving.value = true
      try {
        if (isEditing.value) {
          await axios.put(`/api/v1/colleges/${editedItem.value.id}`, editedItem.value)
          showSuccess('College updated successfully')
        } else {
          await axios.post('/api/v1/colleges/', editedItem.value)
          showSuccess('College added successfully')
        }
        await fetchColleges()
        closeDialog()
      } catch (error) {
        showError(error.response?.data?.detail || 'Error saving college')
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
          await axios.put(`/api/v1/colleges/${item.id}`, {
            ...item,
            is_active: !item.is_active
          })
          await fetchColleges()
          showSuccess(`College ${item.is_active ? 'deactivated' : 'activated'} successfully`)
        } catch (error) {
          showError('Error updating college status')
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
      fetchColleges()
    })

    return {
      // Data
      colleges,
      loading,
      dialog,
      confirmDialog,
      valid,
      saving,
      search,
      stateFilter,
      statusFilter,
      form,
      states,
      headers,
      editedItem,
      isEditing,
      emailRules,
      confirmAction,
      confirmMessage,
      snackbar,
      filteredColleges,

      // Methods
      openAddDialog,
      openEditDialog,
      closeDialog,
      saveCollege,
      toggleStatus
    }
  }
}
</script>

<style scoped>
.colleges-management {
  padding: 20px;
}
</style>
