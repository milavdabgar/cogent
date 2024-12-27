<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h1 class="text-h4">Degree Levels</h1>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="openCreateDialog"
        >
          Add Degree Level
        </v-btn>
      </v-col>
    </v-row>

    <!-- Degree Levels Table -->
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="degreeLevels"
          :loading="loading"
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
                  label="Level Name"
                  :rules="[v => !!v || 'Name is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.code"
                  label="Level Code"
                  :rules="[v => !!v || 'Code is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.duration_years"
                  label="Duration (Years)"
                  type="number"
                  :rules="[v => !!v || 'Duration is required']"
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
        <v-card-title class="text-h5">Delete Degree Level</v-card-title>
        <v-card-text>
          Are you sure you want to delete this degree level?
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
            @click="deleteDegreeLevel"
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

const dialog = ref(false)
const deleteDialog = ref(false)
const loading = ref(false)
const degreeLevels = ref([])

const headers = [
  { title: 'Level Code', key: 'code', sortable: true },
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Duration (Years)', key: 'duration_years', sortable: true },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false },
]

const defaultItem = {
  id: null,
  code: '',
  name: '',
  duration_years: 0,
  description: '',
}

const editedItem = ref({ ...defaultItem })
const editedIndex = ref(-1)

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New Degree Level' : 'Edit Degree Level'
})

const fetchDegreeLevels = async () => {
  try {
    loading.value = true
    degreeLevels.value = await gtuAdminStore.fetchDegreeLevels()
  } catch (error) {
    console.error('Error fetching degree levels:', error)
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
  editedIndex.value = degreeLevels.value.indexOf(item)
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
      await gtuAdminStore.updateDegreeLevel(editedItem.value.id, editedItem.value)
    } else {
      // Create
      await gtuAdminStore.createDegreeLevel(editedItem.value)
    }
    await fetchDegreeLevels()
    closeDialog()
  } catch (error) {
    console.error('Error saving degree level:', error)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (item) => {
  editedItem.value = { ...item }
  deleteDialog.value = true
}

const deleteDegreeLevel = async () => {
  try {
    loading.value = true
    await gtuAdminStore.deleteDegreeLevel(editedItem.value.id)
    await fetchDegreeLevels()
    deleteDialog.value = false
  } catch (error) {
    console.error('Error deleting degree level:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDegreeLevels()
})
</script>
