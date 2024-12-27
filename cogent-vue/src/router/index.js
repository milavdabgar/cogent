import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Role-specific navigation items
const getNavItems = (role) => {
  switch (role) {
    case 'dte_admin':
      return [
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
    case 'admin':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/admin'
        },
        {
          title: 'Users',
          icon: 'mdi-account-group',
          to: '/dashboard/admin/users'
        },
        {
          title: 'Colleges',
          icon: 'mdi-office-building',
          to: '/dashboard/admin/colleges'
        },
        {
          title: 'Courses',
          icon: 'mdi-book-open-variant',
          to: '/dashboard/admin/courses'
        },
        {
          title: 'Settings',
          icon: 'mdi-cog',
          to: '/dashboard/admin/settings'
        }
      ]
    case 'principal':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/principal'
        }
      ]
    case 'hod':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/hod'
        }
      ]
    case 'faculty':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/faculty'
        }
      ]
    case 'student':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/student'
        }
      ]
    default:
      return []
  }
}

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
  // Protected routes with base layout
  {
    path: '/dashboard',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: (route) => {
      const authStore = useAuthStore()
      return {
        title: 'Profile Settings',
        navigationItems: getNavItems(authStore.userRole)
      }
    },
    meta: { requiresAuth: true },
    children: [
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/auth/ProfileView.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },
  // DTE Admin routes
  {
    path: '/dashboard/dte-admin',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true, roles: ['dte_admin'] },
    children: [
      {
        path: '',
        name: 'DTEAdminDashboard',
        component: () => import('@/views/dashboards/DTEAdminDashboard.vue')
      },
      {
        path: 'colleges',
        name: 'DTEAdminColleges',
        component: () => import('@/views/dte-admin/CollegeList.vue')
      },
      {
        path: 'departments',
        name: 'DTEAdminDepartments',
        component: () => import('@/views/dte-admin/DepartmentList.vue')
      }
    ]
  },
  // Admin routes
  {
    path: '/dashboard/admin',
    component: () => import('@/layouts/AdminDashboardLayout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/dashboards/AdminDashboard.vue')
      },
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
  },
  // Other role dashboards
  {
    path: '/dashboard/faculty',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'Faculty Portal',
      navigationItems: getNavItems('faculty')
    },
    children: [
      {
        path: '',
        name: 'FacultyDashboard',
        component: () => import('@/views/dashboards/FacultyDashboard.vue'),
        meta: { requiresAuth: true, role: 'faculty' }
      }
    ]
  },
  {
    path: '/dashboard/student',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'Student Portal',
      navigationItems: getNavItems('student')
    },
    children: [
      {
        path: '',
        name: 'StudentDashboard',
        component: () => import('@/views/dashboards/StudentDashboard.vue'),
        meta: { requiresAuth: true, role: 'student' }
      }
    ]
  },
  {
    path: '/dashboard/hod',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'HOD Portal',
      navigationItems: getNavItems('hod')
    },
    children: [
      {
        path: '',
        name: 'HODDashboard',
        component: () => import('@/views/dashboards/HODDashboard.vue'),
        meta: { requiresAuth: true, role: 'hod' }
      }
    ]
  },
  {
    path: '/dashboard/principal',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'Principal Portal',
      navigationItems: getNavItems('principal')
    },
    children: [
      {
        path: '',
        name: 'PrincipalDashboard',
        component: () => import('@/views/dashboards/PrincipalDashboard.vue'),
        meta: { requiresAuth: true, role: 'principal' }
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
    next('/login')
  } else if (to.meta.role && !authStore.hasRole(to.meta.role)) {
    next(authStore.defaultRoute)
  } else if (to.meta.roles && !authStore.hasAnyRole(to.meta.roles)) {
    next(authStore.defaultRoute)
  } else {
    next()
  }
})

export default router
