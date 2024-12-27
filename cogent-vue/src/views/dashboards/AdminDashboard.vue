<template>
  <v-container fluid>
    <v-row>
      <!-- Summary Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Users</div>
            <div class="text-h4">{{ stats.totalUsers }}</div>
          </v-card-text>
        </v-card>
      </v-col>
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
              <v-col v-for="action in quickActions" :key="action.title" cols="12" sm="6" md="3">
                <v-btn
                  block
                  :color="action.color"
                  :to="action.route"
                  class="mb-2"
                >
                  <v-icon start>{{ action.icon }}</v-icon>
                  {{ action.title }}
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Recent Activities -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Recent Activities</v-card-title>
          <v-card-text>
            <v-timeline density="compact">
              <v-timeline-item
                v-for="activity in recentActivities"
                :key="activity.id"
                :dot-color="activity.color"
                size="small"
              >
                <div class="mb-2">
                  <div class="text-subtitle-2">{{ activity.title }}</div>
                  <div class="text-caption">{{ activity.timestamp }}</div>
                  <div class="text-body-2">{{ activity.description }}</div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- System Health -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>System Health</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="status in systemStatus"
                :key="status.service"
                :title="status.service"
                :subtitle="status.status"
              >
                <template v-slot:prepend>
                  <v-icon
                    :color="status.status === 'Operational' ? 'success' : 'error'"
                  >
                    {{ status.status === 'Operational' ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                  </v-icon>
                </template>
                <template v-slot:append>
                  <v-chip
                    :color="status.status === 'Operational' ? 'success' : 'error'"
                    size="small"
                  >
                    {{ status.uptime }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({
  totalUsers: 0,
  totalColleges: 0,
  activeStudents: 0,
  activeFaculty: 0
})

const quickActions = ref([
  {
    title: 'Manage Users',
    icon: 'mdi-account-group',
    route: '/admin/users',
    color: 'primary'
  },
  {
    title: 'Manage Colleges',
    icon: 'mdi-school',
    route: '/admin/colleges',
    color: 'secondary'
  },
  {
    title: 'Manage Courses',
    icon: 'mdi-book-open-variant',
    route: '/admin/courses',
    color: 'success'
  },
  {
    title: 'System Settings',
    icon: 'mdi-cog',
    route: '/admin/settings',
    color: 'info'
  }
])

const recentActivities = ref([
  {
    id: 1,
    title: 'New College Added',
    description: 'Added GTU College of Engineering',
    timestamp: '10 minutes ago',
    color: 'success'
  },
  {
    id: 2,
    title: 'User Role Updated',
    description: 'Updated role for John Doe to HOD',
    timestamp: '1 hour ago',
    color: 'info'
  },
  {
    id: 3,
    title: 'New Batch Created',
    description: 'Created new batch for CS 2024',
    timestamp: '2 hours ago',
    color: 'primary'
  }
])

const systemStatus = ref([
  {
    service: 'Authentication Service',
    status: 'Operational',
    uptime: '99.9%'
  },
  {
    service: 'Database',
    status: 'Operational',
    uptime: '99.8%'
  },
  {
    service: 'File Storage',
    status: 'Operational',
    uptime: '99.9%'
  },
  {
    service: 'API Services',
    status: 'Operational',
    uptime: '99.7%'
  }
])

// Fetch dashboard stats
const fetchStats = async () => {
  try {
    const response = await axios.get('/api/v1/admin/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Error fetching admin stats:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>
