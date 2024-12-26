<template>
  <v-container fluid>
    <v-row>
      <!-- Department Stats -->
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Faculty</div>
            <div class="text-h4">25</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Total Students</div>
            <div class="text-h4">450</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Ongoing Projects</div>
            <div class="text-h4">8</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-subtitle-1">Department Rank</div>
            <div class="text-h4">#2</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Faculty Performance -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Faculty Performance</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(faculty, i) in facultyPerformance"
                :key="i"
                :title="faculty.name"
                :subtitle="faculty.subject"
              >
                <template v-slot:append>
                  <v-rating
                    :model-value="faculty.rating"
                    color="amber"
                    density="compact"
                    readonly
                    size="small"
                  ></v-rating>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Department Updates -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Recent Department Updates</v-card-title>
          <v-card-text>
            <v-timeline density="compact">
              <v-timeline-item
                v-for="(update, i) in departmentUpdates"
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

const facultyPerformance = ref([
  {
    name: 'Dr. Sarah Wilson',
    subject: 'Advanced Computing',
    rating: 4.5
  },
  {
    name: 'Prof. James Anderson',
    subject: 'Network Security',
    rating: 4.8
  },
  {
    name: 'Dr. Emily Brown',
    subject: 'Data Science',
    rating: 4.2
  }
])

const departmentUpdates = ref([
  {
    title: 'New Research Grant',
    description: 'Department secured $500K research grant for AI Lab',
    date: '2 days ago',
    color: 'success'
  },
  {
    title: 'Faculty Meeting',
    description: 'Monthly faculty meeting scheduled for next week',
    date: '1 week ago',
    color: 'primary'
  },
  {
    title: 'Student Achievement',
    description: 'Students won first prize in national hackathon',
    date: '2 weeks ago',
    color: 'info'
  }
])
</script>
