<template>
  <v-container fluid>
    <v-row>
      <!-- Institution Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Students</div>
            <div class="text-h4">2,500</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Faculty</div>
            <div class="text-h4">150</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Departments</div>
            <div class="text-h4">8</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Placement Rate</div>
            <div class="text-h4">92%</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Department Performance -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Department Performance</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(dept, i) in departmentPerformance"
                :key="i"
                :title="dept.name"
                :subtitle="'HOD: ' + dept.hod"
              >
                <template v-slot:append>
                  <v-chip
                    :color="getPerformanceColor(dept.performance)"
                    size="small"
                  >
                    {{ dept.performance }}%
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Recent Updates -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Institution Updates</v-card-title>
          <v-card-text>
            <v-timeline density="compact">
              <v-timeline-item
                v-for="(update, i) in institutionUpdates"
                :key="i"
                :dot-color="update.color"
                size="small"
              >
                <div class="mb-4">
                  <div class="text-h6">{{ update.title }}</div>
                  <div>{{ update.description }}</div>
                  <div class="text-caption">{{ update.date }}</div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const departmentPerformance = ref([
  {
    name: 'Computer Science',
    hod: 'Dr. Robert Wilson',
    performance: 95
  },
  {
    name: 'Electrical Engineering',
    hod: 'Dr. Maria Garcia',
    performance: 88
  },
  {
    name: 'Mechanical Engineering',
    hod: 'Dr. James Thompson',
    performance: 92
  },
  {
    name: 'Civil Engineering',
    hod: 'Dr. Sarah Anderson',
    performance: 85
  }
])

const institutionUpdates = ref([
  {
    title: 'NAAC Accreditation',
    description: 'Institution received A++ grade in NAAC evaluation',
    date: '1 week ago',
    color: 'success'
  },
  {
    title: 'Industry Partnership',
    description: 'New MoU signed with leading tech companies',
    date: '2 weeks ago',
    color: 'primary'
  },
  {
    title: 'Research Grant',
    description: 'Received government grant for research excellence',
    date: '1 month ago',
    color: 'info'
  }
])

const getPerformanceColor = (performance) => {
  if (performance >= 90) return 'success'
  if (performance >= 80) return 'primary'
  return 'warning'
}
</script>
