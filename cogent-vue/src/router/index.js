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
    component: () => import('@/views/auth/Login.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('@/views/auth/Signup.vue')
  },
  {
    path: '/password-reset',
    name: 'PasswordReset',
    component: () => import('@/views/auth/PasswordResetView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/auth/ProfileView.vue'),
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
  },
  {
    path: '/dashboard/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/dashboards/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  // Admin management routes
  {
    path: '/admin',
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: 'users',
        name: 'ManageUsers',
        component: () => import('@/views/admin/UsersManagement.vue')
      },
      {
        path: 'colleges',
        name: 'ManageColleges',
        component: () => import('@/views/admin/CollegesManagement.vue')
      },
      {
        path: 'courses',
        name: 'ManageCourses',
        component: () => import('@/views/admin/CoursesManagement.vue')
      },
      {
        path: 'settings',
        name: 'SystemSettings',
        component: () => import('@/views/admin/SystemSettings.vue')
      }
    ]
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
