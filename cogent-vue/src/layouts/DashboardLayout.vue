<template>
  <BaseDashboardLayout
    title="DTE Admin Portal"
    :navigation-items="navigationItems"
  />
</template>

<script setup>
import BaseDashboardLayout from './BaseDashboardLayout.vue'

const navigationItems = [
  {
    title: 'Dashboard',
    icon: 'mdi-view-dashboard',
    to: '/dashboard/dte-admin'
  },
  {
    title: 'Colleges',
    icon: 'mdi-office-building',
    to: '/dashboard/dte-admin/colleges'
  },
  {
    title: 'Departments',
    icon: 'mdi-domain',
    to: '/dashboard/dte-admin/departments'
  }
]
</script>

<style scoped>
.v-navigation-drawer {
  border-right: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
