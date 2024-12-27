<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h1 class="text-h4">Departments</h1>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="openCreateDialog"
        >
          Add Department
        </v-btn>
      </v-col>
    </v-row>

    <!-- Search and Filter -->
    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-text-field
          v-model="search"
          label="Search Departments"
          prepend-icon="mdi-magnify"
          clearable
          hide-details
          class="mb-4"
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- Departments Table -->
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="departments"
          :loading="loading"
          :search="search"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              variant="text"
              color="primary"
              @click="openEditDialog(item.raw)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              variant="text"
              color="error"
              @click="confirmDelete(item.raw)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.name"
                  label="Department Name"
                  :rules="[v => !!v || 'Name is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.code"
                  label="Department Code"
                  :rules="[v => !!v || 'Code is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.description"
                  label="Description"
                  rows="3"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="save"
          >
            Save
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="closeDialog"
          >
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Delete Department</v-card-title>
        <v-card-text>
          Are you sure you want to delete this department?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="deleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="deleteDepartment"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGTUAdminStore } from '@/stores/gtu-admin'

const gtuAdminStore = useGTUAdminStore()

const search = ref('')
const dialog = ref(false)
const deleteDialog = ref(false)
const loading = ref(false)
const departments = ref([])

const headers = [
  { title: 'Department Code', key: 'code', sortable: true },
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false },
]

const defaultItem = {
  id: null,
  code: '',
  name: '',
  description: '',
}

const editedItem = ref({ ...defaultItem })
const editedIndex = ref(-1)

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New Department' : 'Edit Department'
})

const fetchDepartments = async () => {
  try {
    loading.value = true
    departments.value = await gtuAdminStore.fetchDepartments()
  } catch (error) {
    console.error('Error fetching departments:', error)
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  editedIndex.value = -1
  editedItem.value = { ...defaultItem }
  dialog.value = true
}

const openEditDialog = (item) => {
  editedIndex.value = departments.value.indexOf(item)
  editedItem.value = { ...item }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editedItem.value = { ...defaultItem }
  editedIndex.value = -1
}

const save = async () => {
  try {
    loading.value = true
    if (editedIndex.value > -1) {
      // Update
      await gtuAdminStore.updateDepartment(editedItem.value.id, editedItem.value)
    } else {
      // Create
      await gtuAdminStore.createDepartment(editedItem.value)
    }
    await fetchDepartments()
    closeDialog()
  } catch (error) {
    console.error('Error saving department:', error)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (item) => {
  editedItem.value = { ...item }
  deleteDialog.value = true
}

const deleteDepartment = async () => {
  try {
    loading.value = true
    await gtuAdminStore.deleteDepartment(editedItem.value.id)
    await fetchDepartments()
    deleteDialog.value = false
  } catch (error) {
    console.error('Error deleting department:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDepartments()
})
</script>
