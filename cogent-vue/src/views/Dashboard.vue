<template>
  <div class="dashboard-container">
    <router-view></router-view>
  </div>
</template>

<style>
.dashboard-container {
  height: 100%;
  width: 100%;
}
</style>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
