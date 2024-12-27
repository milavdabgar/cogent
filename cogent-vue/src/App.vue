<template>
  <v-app>
    <v-main class="fill-height">
      <router-view v-slot="{ Component }">
        <v-container fluid class="fill-height pa-0">
          <component :is="Component" />
        </v-container>
      </router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.v-application {
  min-height: 100vh !important;
  height: 100vh !important;
  width: 100vw !important;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.v-main {
  flex: 1 1 auto;
  height: 100vh !important;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.v-container {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  height: 100% !important;
  overflow: auto;
}

.fill-height {
  height: 100% !important;
  min-height: 100% !important;
}
</style>
