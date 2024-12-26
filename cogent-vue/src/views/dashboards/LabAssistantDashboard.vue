<template>
  <v-container fluid>
    <v-row>
      <!-- Lab Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Equipment</div>
            <div class="text-h4">75</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Lab Sessions Today</div>
            <div class="text-h4">6</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Pending Maintenance</div>
            <div class="text-h4">3</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Equipment Status</div>
            <div class="text-h4">95%</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Lab Schedule -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Today's Lab Schedule</v-card-title>
          <v-card-text>
            <v-timeline density="compact">
              <v-timeline-item
                v-for="(session, i) in labSchedule"
                :key="i"
                :dot-color="session.color"
                size="small"
              >
                <template v-slot:opposite>
                  {{ session.time }}
                </template>
                <div class="mb-4">
                  <div class="text-h6">{{ session.subject }}</div>
                  <div>{{ session.faculty }}</div>
                  <div class="text-caption">
                    Lab: {{ session.lab }} | Batch: {{ session.batch }}
                  </div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Maintenance Tasks -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Maintenance Tasks</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(task, i) in maintenanceTasks"
                :key="i"
                :title="task.equipment"
                :subtitle="task.description"
              >
                <template v-slot:append>
                  <v-chip
                    :color="task.priority === 'High' ? 'error' : 'warning'"
                    size="small"
                  >
                    {{ task.priority }}
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
import { ref } from 'vue'

const labSchedule = ref([
  {
    time: '9:00 AM',
    subject: 'Computer Networks Lab',
    faculty: 'Prof. Johnson',
    lab: 'Network Lab',
    batch: 'CS-3rd Year',
    color: 'primary'
  },
  {
    time: '11:00 AM',
    subject: 'Database Lab',
    faculty: 'Dr. Smith',
    lab: 'Database Lab',
    batch: 'CS-2nd Year',
    color: 'success'
  },
  {
    time: '2:00 PM',
    subject: 'Programming Lab',
    faculty: 'Prof. Davis',
    lab: 'Programming Lab',
    batch: 'CS-1st Year',
    color: 'warning'
  }
])

const maintenanceTasks = ref([
  {
    equipment: 'Network Switch',
    description: 'Replace faulty ports',
    priority: 'High'
  },
  {
    equipment: 'Workstation PC-15',
    description: 'Software update required',
    priority: 'Medium'
  },
  {
    equipment: 'Printer Lab-2',
    description: 'Cartridge replacement',
    priority: 'Medium'
  }
])
</script>
