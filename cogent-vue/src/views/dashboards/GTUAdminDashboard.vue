<template>
  <v-container>
    <v-row>
      <!-- Statistics Cards -->
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="344">
          <v-card-text>
            <div class="text-subtitle-1 text-medium-emphasis">Total Departments</div>
            <div class="text-h4 text-primary">{{ departments.length }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="344">
          <v-card-text>
            <div class="text-subtitle-1 text-medium-emphasis">Degree Programs</div>
            <div class="text-h4 text-primary">{{ degreePrograms.length }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="344">
          <v-card-text>
            <div class="text-subtitle-1 text-medium-emphasis">Total Subjects</div>
            <div class="text-h4 text-primary">{{ subjects.length }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Actions -->
    <v-row class="mt-6">
      <v-col cols="12">
        <h2 class="text-h5 mb-4">Quick Actions</h2>
        <v-btn
          color="primary"
          class="mr-4"
          :to="{ name: 'GTUAdminDepartments' }"
        >
          MANAGE DEPARTMENTS
        </v-btn>
        <v-btn
          color="primary"
          class="mr-4"
          :to="{ name: 'GTUAdminDegreeLevels' }"
        >
          MANAGE DEGREE LEVELS
        </v-btn>
        <v-btn
          color="primary"
          class="mr-4"
          :to="{ name: 'GTUAdminDegreePrograms' }"
        >
          MANAGE PROGRAMS
        </v-btn>
        <v-btn
          color="primary"
          :to="{ name: 'GTUAdminSubjects' }"
        >
          MANAGE SUBJECTS
        </v-btn>
      </v-col>
    </v-row>

    <!-- Recent Activities -->
    <v-row class="mt-6">
      <v-col cols="12">
        <h2 class="text-h5 mb-4">Recent Activities</h2>
        <v-timeline side="end">
          <v-timeline-item
            v-for="activity in recentActivities"
            :key="activity.id"
            :dot-color="activity.color"
            size="small"
          >
            <div class="d-flex">
              <div>
                <div class="text-h6">{{ activity.title }}</div>
                <div class="text-caption">{{ activity.description }}</div>
              </div>
            </div>
          </v-timeline-item>
        </v-timeline>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useGTUAdminStore } from '@/stores/gtu-admin'

const gtuAdminStore = useGTUAdminStore()

const departments = ref([])
const degreePrograms = ref([])
const subjects = ref([])
const recentActivities = ref([
  {
    id: 1,
    title: 'New Department Added',
    description: 'Added Computer Engineering department',
    color: 'primary',
  },
])

onMounted(async () => {
  try {
    departments.value = await gtuAdminStore.fetchDepartments()
    degreePrograms.value = await gtuAdminStore.fetchDegreePrograms()
    subjects.value = await gtuAdminStore.fetchSubjects()
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
})
</script>

<style scoped>
.v-timeline {
  max-height: 400px;
  overflow-y: auto;
}
</style>
