<template>
  <v-app>
    <v-navigation-drawer
      v-if="authStore.isAuthenticated"
      v-model="drawer"
      :rail="rail"
      permanent
      class="fill-height"
    >
      <template #default>
        <v-list>
          <v-list-item
            prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
            :title="authStore.fullName"
          >
            <template #append>
              <v-btn
                variant="text"
                icon="mdi-chevron-left"
                @click.stop="rail = !rail"
              ></v-btn>
            </template>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item :to="authStore.defaultRoute" prepend-icon="mdi-view-dashboard" title="Dashboard"></v-list-item>
          <v-list-item to="/profile" prepend-icon="mdi-account" title="Profile"></v-list-item>
          <v-list-item @click="handleLogout" prepend-icon="mdi-logout" title="Logout"></v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const drawer = ref(true)
const rail = ref(true)

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

.v-navigation-drawer {
  height: 100vh !important;
}
</style>
