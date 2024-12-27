<template>
  <BaseDashboardLayout
    title="Admin Portal"
    :navigation-items="navigationItems"
  />
</template>

<script setup>
import BaseDashboardLayout from './BaseDashboardLayout.vue'

const navigationItems = [
  {
    title: 'Dashboard',
    icon: 'mdi-view-dashboard',
    to: '/dashboard/admin'
  },
  {
    title: 'Users',
    icon: 'mdi-account-group',
    to: '/admin/users'
  },
  {
    title: 'Colleges',
    icon: 'mdi-office-building',
    to: '/admin/colleges'
  },
  {
    title: 'Courses',
    icon: 'mdi-book-open-variant',
    to: '/admin/courses'
  },
  {
    title: 'Settings',
    icon: 'mdi-cog',
    to: '/admin/settings'
  }
]
</script>
