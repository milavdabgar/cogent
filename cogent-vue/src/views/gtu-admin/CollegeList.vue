<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Manage Colleges</h1>
      </v-col>
    </v-row>

    <!-- Search and Filter -->
    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-text-field
          v-model="search"
          label="Search Colleges"
          prepend-icon="mdi-magnify"
          clearable
          @update:model-value="fetchColleges"
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- Colleges Table -->
    <v-row>
      <v-col cols="12">
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
              color="primary"
              @click="viewCollege(item)"
            >
              <v-icon>mdi-eye</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- View College Dialog -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card v-if="selectedCollege">
        <v-card-title>
          <span class="text-h5">{{ selectedCollege.name }}</span>
        </v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-title>Code</v-list-item-title>
              <v-list-item-subtitle>{{ selectedCollege.code }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>City</v-list-item-title>
              <v-list-item-subtitle>{{ selectedCollege.city }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Address</v-list-item-title>
              <v-list-item-subtitle>{{ selectedCollege.address }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="viewDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useGTUAdminStore } from '@/stores/gtu-admin'

const gtuAdminStore = useGTUAdminStore()

const search = ref('')
const loading = ref(false)
const colleges = ref([])
const viewDialog = ref(false)
const selectedCollege = ref(null)

const headers = [
  { title: 'Code', key: 'code' },
  { title: 'Name', key: 'name' },
  { title: 'City', key: 'city' },
  { title: 'Actions', key: 'actions', sortable: false },
]

const fetchColleges = async () => {
  try {
    loading.value = true
    colleges.value = await gtuAdminStore.fetchColleges()
  } catch (error) {
    console.error('Error fetching colleges:', error)
  } finally {
    loading.value = false
  }
}

const viewCollege = (item) => {
  selectedCollege.value = item.raw
  viewDialog.value = true
}

onMounted(() => {
  fetchColleges()
})
</script>
