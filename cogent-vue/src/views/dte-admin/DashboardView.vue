<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-6">DTE Admin Dashboard</h1>
    
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div v-for="(stat, key) in stats" :key="key" 
           class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 class="text-gray-500 text-sm font-medium mb-2">{{ formatStatLabel(key) }}</h3>
        <p class="text-3xl font-semibold">{{ stat }}</p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 class="text-lg font-semibold mb-4">Quick Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <router-link 
          to="/dte-admin/colleges"
          class="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
          <span class="material-icons mr-2">school</span>
          Manage Colleges
        </router-link>
        <!-- Add more quick actions as needed -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDTEAdminStore } from '@/stores/dte-admin'

const dteAdminStore = useDTEAdminStore()
const stats = ref(null)

onMounted(async () => {
  await dteAdminStore.fetchStats()
  stats.value = dteAdminStore.stats
})

const formatStatLabel = (key) => {
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
</script>
