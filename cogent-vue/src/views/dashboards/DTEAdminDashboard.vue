<template>
  <v-container fluid>
    <v-row>
      <!-- Summary Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Colleges</div>
            <div class="text-h4">{{ stats.totalColleges }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Departments</div>
            <div class="text-h4">{{ stats.totalDepartments }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Active Students</div>
            <div class="text-h4">{{ stats.activeStudents }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Active Faculty</div>
            <div class="text-h4">{{ stats.activeFaculty }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Quick Actions -->
      <v-col cols="12">
        <v-card>
          <v-card-title>Quick Actions</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="primary"
                  to="/dte-admin/colleges"
                  class="mb-2"
                >
                  <v-icon start>mdi-office-building</v-icon>
                  Manage Colleges
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="secondary"
                  to="/dte-admin/departments"
                  class="mb-2"
                >
                  <v-icon start>mdi-domain</v-icon>
                  Manage Departments
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Recent Activities -->
      <v-col cols="12">
        <v-card>
          <v-card-title>Recent Activities</v-card-title>
          <v-list>
            <v-list-item
              v-for="activity in recentActivities"
              :key="activity.id"
              :title="activity.title"
              :subtitle="activity.description"
              :prepend-icon="activity.icon || 'mdi-bell'"
            />
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDTEAdminStore } from '@/stores/dte-admin'

const dteAdminStore = useDTEAdminStore()

const stats = ref({
  totalColleges: 0,
  totalDepartments: 0,
  activeStudents: 0,
  activeFaculty: 0
})

const recentActivities = ref([
  {
    id: 1,
    title: 'New College Added',
    description: 'Added GTU College of Engineering',
    icon: 'mdi-office-building'
  },
  {
    id: 2,
    title: 'Department Updated',
    description: 'Updated Computer Science Department',
    icon: 'mdi-domain'
  }
])

const fetchStats = async () => {
  await dteAdminStore.fetchStats()
  stats.value = dteAdminStore.stats || stats.value
}

onMounted(() => {
  fetchStats()
})
</script>
