<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h1 class="text-h4">Degree Programs</h1>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="openCreateDialog"
        >
          Add Program
        </v-btn>
      </v-col>
    </v-row>

    <!-- Programs Table -->
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="degreePrograms"
          :loading="loading"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              variant="text"
              color="info"
              @click="viewSubjects(item.raw)"
              title="View Subjects"
            >
              <v-icon>mdi-book-open-variant</v-icon>
            </v-btn>
            <v-btn
              icon
              variant="text"
              color="primary"
              @click="openEditDialog(item.raw)"
              title="Edit"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              variant="text"
              color="error"
              @click="confirmDelete(item.raw)"
              title="Delete"
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
                  label="Program Name"
                  :rules="[v => !!v || 'Name is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.code"
                  label="Program Code"
                  :rules="[v => !!v || 'Code is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.degree_level_id"
                  :items="degreeLevels"
                  item-title="name"
                  item-value="id"
                  label="Degree Level"
                  :rules="[v => !!v || 'Degree Level is required']"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.department_id"
                  :items="departments"
                  item-title="name"
                  item-value="id"
                  label="Department"
                  :rules="[v => !!v || 'Department is required']"
                  required
                ></v-select>
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
        <v-card-title class="text-h5">Delete Program</v-card-title>
        <v-card-text>
          Are you sure you want to delete this program?
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
            @click="deleteDegreeProgram"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- View Subjects Dialog -->
    <v-dialog v-model="subjectsDialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Program Subjects</span>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            @click="openAddSubjectDialog"
            v-if="selectedProgram"
          >
            Add Subject
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-data-table
            :headers="subjectHeaders"
            :items="programSubjects"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                variant="text"
                color="error"
                @click="removeSubject(item.raw)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="subjectsDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Add Subject Dialog -->
    <v-dialog v-model="addSubjectDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Add Subject to Program</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-select
                  v-model="selectedSubject"
                  :items="availableSubjects"
                  item-title="name"
                  item-value="id"
                  label="Subject"
                  :rules="[v => !!v || 'Subject is required']"
                  required
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="addSubject"
          >
            Add
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="addSubjectDialog = false"
          >
            Cancel
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
const subjectsDialog = ref(false)
const addSubjectDialog = ref(false)
const loading = ref(false)
const degreePrograms = ref([])
const degreeLevels = ref([])
const departments = ref([])
const programSubjects = ref([])
const availableSubjects = ref([])
const selectedProgram = ref(null)
const selectedSubject = ref(null)

const headers = [
  { title: 'Program Code', key: 'code', sortable: true },
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Department', key: 'department.name', sortable: true },
  { title: 'Degree Level', key: 'degree_level.name', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false },
]

const subjectHeaders = [
  { title: 'Subject Code', key: 'code', sortable: true },
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Credits', key: 'credits', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false },
]

const defaultItem = {
  id: null,
  code: '',
  name: '',
  department_id: null,
  degree_level_id: null,
  description: '',
}

const editedItem = ref({ ...defaultItem })
const editedIndex = ref(-1)

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New Program' : 'Edit Program'
})

const fetchDegreePrograms = async () => {
  try {
    loading.value = true
    degreePrograms.value = await gtuAdminStore.fetchDegreePrograms()
  } catch (error) {
    console.error('Error fetching degree programs:', error)
  } finally {
    loading.value = false
  }
}

const fetchDegreeLevels = async () => {
  try {
    degreeLevels.value = await gtuAdminStore.fetchDegreeLevels()
  } catch (error) {
    console.error('Error fetching degree levels:', error)
  }
}

const fetchDepartments = async () => {
  try {
    departments.value = await gtuAdminStore.fetchDepartments()
  } catch (error) {
    console.error('Error fetching departments:', error)
  }
}

const openCreateDialog = () => {
  editedIndex.value = -1
  editedItem.value = { ...defaultItem }
  dialog.value = true
}

const openEditDialog = (item) => {
  editedIndex.value = degreePrograms.value.indexOf(item)
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
      await gtuAdminStore.updateDegreeProgram(editedItem.value.id, editedItem.value)
    } else {
      // Create
      await gtuAdminStore.createDegreeProgram(editedItem.value)
    }
    await fetchDegreePrograms()
    closeDialog()
  } catch (error) {
    console.error('Error saving degree program:', error)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (item) => {
  editedItem.value = { ...item }
  deleteDialog.value = true
}

const deleteDegreeProgram = async () => {
  try {
    loading.value = true
    await gtuAdminStore.deleteDegreeProgram(editedItem.value.id)
    await fetchDegreePrograms()
    deleteDialog.value = false
  } catch (error) {
    console.error('Error deleting degree program:', error)
  } finally {
    loading.value = false
  }
}

const viewSubjects = async (item) => {
  try {
    loading.value = true
    selectedProgram.value = item
    programSubjects.value = await gtuAdminStore.getProgramSubjects(item.id)
    subjectsDialog.value = true
  } catch (error) {
    console.error('Error fetching program subjects:', error)
  } finally {
    loading.value = false
  }
}

const openAddSubjectDialog = async () => {
  try {
    loading.value = true
    availableSubjects.value = await gtuAdminStore.fetchSubjects()
    // Filter out subjects already in the program
    const programSubjectIds = programSubjects.value.map(s => s.id)
    availableSubjects.value = availableSubjects.value.filter(s => !programSubjectIds.includes(s.id))
    addSubjectDialog.value = true
  } catch (error) {
    console.error('Error fetching available subjects:', error)
  } finally {
    loading.value = false
  }
}

const addSubject = async () => {
  try {
    loading.value = true
    await gtuAdminStore.mapSubjectToProgram({
      program_id: selectedProgram.value.id,
      subject_id: selectedSubject.value,
    })
    await viewSubjects(selectedProgram.value)
    addSubjectDialog.value = false
    selectedSubject.value = null
  } catch (error) {
    console.error('Error adding subject to program:', error)
  } finally {
    loading.value = false
  }
}

const removeSubject = async (subject) => {
  try {
    loading.value = true
    await gtuAdminStore.unmapSubjectFromProgram(selectedProgram.value.id, subject.id)
    await viewSubjects(selectedProgram.value)
  } catch (error) {
    console.error('Error removing subject from program:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    fetchDegreePrograms(),
    fetchDegreeLevels(),
    fetchDepartments(),
  ])
})
</script>
