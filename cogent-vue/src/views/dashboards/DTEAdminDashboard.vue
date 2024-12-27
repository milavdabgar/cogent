<template>
  <v-container>
    <v-row>
      <!-- Statistics Cards -->
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="344">
          <v-card-text>
            <div class="text-subtitle-1 text-medium-emphasis">Total Colleges</div>
            <div class="text-h4 text-primary">{{ totalColleges }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="344">
          <v-card-text>
            <div class="text-subtitle-1 text-medium-emphasis">Active Students</div>
            <div class="text-h4 text-primary">{{ activeStudents }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="344">
          <v-card-text>
            <div class="text-subtitle-1 text-medium-emphasis">Active Faculty</div>
            <div class="text-h4 text-primary">{{ activeFaculty }}</div>
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
          :to="{ name: 'colleges' }"
        >
          MANAGE COLLEGES
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
import { useDTEAdminStore } from '@/stores/dte-admin'

const dteAdminStore = useDTEAdminStore()

const totalColleges = ref(0)
const activeStudents = ref(0)
const activeFaculty = ref(0)
const recentActivities = ref([
  {
    id: 1,
    title: 'New College Added',
    description: 'Added GTU College of Engineering',
    color: 'primary',
  },
])

onMounted(async () => {
  try {
    const stats = await dteAdminStore.fetchDashboardStats()
    totalColleges.value = stats.total_colleges || 0
    activeStudents.value = stats.active_students || 0
    activeFaculty.value = stats.active_faculty || 0
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
