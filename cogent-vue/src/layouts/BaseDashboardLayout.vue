<template>
  <v-app>
    <v-app-bar color="primary" app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      class="fill-height"
    >
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
          :title="authStore.fullName"
          :subtitle="authStore.userRole"
        >
          <template v-slot:append>
            <v-btn
              variant="text"
              icon="mdi-account-edit"
              to="/dashboard/profile"
            ></v-btn>
          </template>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in navigationItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
        ></v-list-item>

        <v-divider class="my-2"></v-divider>
        
        <v-list-item
          to="/dashboard/profile"
          prepend-icon="mdi-account-cog"
          title="Profile Settings"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  navigationItems: {
    type: Array,
    required: true,
    validator: (items) => items.every(item => 
      item.title && item.icon && typeof item.to !== 'undefined'
    )
  }
})

const router = useRouter()
const authStore = useAuthStore()
const drawer = ref(true)

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.v-navigation-drawer {
  border-right: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
