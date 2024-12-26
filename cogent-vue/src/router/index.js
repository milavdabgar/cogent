import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('@/views/Signup.vue')
  },
  {
    path: '/password-reset',
    name: 'PasswordReset',
    component: () => import('@/views/auth/PasswordResetView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/faculty',
    name: 'FacultyDashboard',
    component: () => import('@/views/dashboards/FacultyDashboard.vue'),
    meta: { requiresAuth: true, role: 'faculty' }
  },
  {
    path: '/dashboard/student',
    name: 'StudentDashboard',
    component: () => import('@/views/dashboards/StudentDashboard.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/dashboard/hod',
    name: 'HODDashboard',
    component: () => import('@/views/dashboards/HODDashboard.vue'),
    meta: { requiresAuth: true, role: 'hod' }
  },
  {
    path: '/dashboard/lab-assistant',
    name: 'LabAssistantDashboard',
    component: () => import('@/views/dashboards/LabAssistantDashboard.vue'),
    meta: { requiresAuth: true, role: 'lab_assistant' }
  },
  {
    path: '/dashboard/principal',
    name: 'PrincipalDashboard',
    component: () => import('@/views/dashboards/PrincipalDashboard.vue'),
    meta: { requiresAuth: true, role: 'principal' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.role && authStore.userRole !== to.meta.role) {
    next({ name: authStore.defaultRoute })
  } else {
    next()
  }
})

export default router
