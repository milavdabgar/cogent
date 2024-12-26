<template>
  <v-container fluid>
    <v-row>
      <!-- Quick Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Attendance</div>
            <div class="text-h4 mb-2">85%</div>
            <v-progress-linear
              model-value="85"
              color="primary"
              height="8"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Assignments</div>
            <div class="text-h4 mb-2">8/10</div>
            <v-progress-linear
              model-value="80"
              color="success"
              height="8"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Current CGPA</div>
            <div class="text-h4">3.8</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Upcoming Tests</div>
            <div class="text-h4">3</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Upcoming Classes -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Today's Classes</v-card-title>
          <v-card-text>
            <v-timeline density="compact">
              <v-timeline-item
                v-for="(item, i) in todayClasses"
                :key="i"
                :dot-color="item.color"
                size="small"
              >
                <template v-slot:opposite>
                  {{ item.time }}
                </template>
                <div class="mb-4">
                  <div class="text-h6">{{ item.subject }}</div>
                  <div>{{ item.faculty }}</div>
                  <div class="text-caption">
                    Room: {{ item.room }}
                  </div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Pending Assignments -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Pending Assignments</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(assignment, i) in pendingAssignments"
                :key="i"
                :subtitle="assignment.subject"
                :title="assignment.title"
              >
                <template v-slot:append>
                  <v-chip
                    :color="getDueDateColor(assignment.dueDate)"
                    size="small"
                  >
                    Due: {{ assignment.dueDate }}
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

const todayClasses = ref([
  {
    time: '9:00 AM',
    subject: 'Mathematics',
    faculty: 'Dr. Smith',
    room: '101',
    color: 'primary'
  },
  {
    time: '10:30 AM',
    subject: 'Computer Science',
    faculty: 'Prof. Johnson',
    room: '205',
    color: 'success'
  },
  {
    time: '2:00 PM',
    subject: 'Physics Lab',
    faculty: 'Dr. Williams',
    room: 'Lab 3',
    color: 'warning'
  }
])

const pendingAssignments = ref([
  {
    title: 'Linear Algebra Assignment',
    subject: 'Mathematics',
    dueDate: '2024-01-02'
  },
  {
    title: 'Programming Project',
    subject: 'Computer Science',
    dueDate: '2024-01-05'
  },
  {
    title: 'Lab Report',
    subject: 'Physics',
    dueDate: '2024-01-03'
  }
])

const getDueDateColor = (dueDate) => {
  const today = new Date()
  const due = new Date(dueDate)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'error'
  if (diffDays <= 2) return 'warning'
  return 'success'
}
</script>
