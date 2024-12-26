<template>
  <v-container fluid class="fill-height pa-4">
    <v-row>
      <!-- Quick Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Students</div>
            <div class="text-h4">120</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Classes Today</div>
            <div class="text-h4">4</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Pending Assignments</div>
            <div class="text-h4">8</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Average Attendance</div>
            <div class="text-h4">85%</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Class Schedule -->
      <v-col cols="12" md="6">
        <v-card height="100%">
          <v-card-title>Today's Schedule</v-card-title>
          <v-card-text>
            <v-timeline density="compact">
              <v-timeline-item
                v-for="(class_, i) in todayClasses"
                :key="i"
                :dot-color="class_.color"
                size="small"
              >
                <div class="d-flex justify-space-between">
                  <div>
                    <div class="text-subtitle-2">{{ class_.subject }}</div>
                    <div class="text-caption">{{ class_.room }}</div>
                  </div>
                  <div class="text-caption">{{ class_.time }}</div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Recent Submissions -->
      <v-col cols="12" md="6">
        <v-card height="100%">
          <v-card-title>Recent Assignment Submissions</v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item
                v-for="(submission, i) in recentSubmissions"
                :key="i"
                :title="submission.student"
                :subtitle="submission.assignment"
              >
                <template v-slot:append>
                  <div class="text-caption">{{ submission.time }}</div>
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
    subject: 'Data Structure',
    room: 'Room: 201 | CS-2nd Year',
    time: '10:00 AM',
    color: 'primary'
  },
  {
    subject: 'Database Management',
    room: 'Room: 102 | CS-3rd Year',
    time: '11:30 AM',
    color: 'success'
  }
])

const recentSubmissions = ref([
  {
    student: 'Alice Johnson',
    assignment: 'Data Structure Assignment 3',
    time: '2 hours ago'
  },
  {
    student: 'Bob Smith',
    assignment: 'Database Project Phase 1',
    time: '3 hours ago'
  }
])
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>
