import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Role-specific navigation items
const getNavItems = (role) => {
  switch (role) {
    case 'GTU_ADMIN':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/gtu-admin'
        },
        {
          title: 'Departments',
          icon: 'mdi-domain',
          to: '/dashboard/gtu-admin/departments'
        },
        {
          title: 'Degree Levels',
          icon: 'mdi-school',
          to: '/dashboard/gtu-admin/degree-levels'
        },
        {
          title: 'Degree Programs',
          icon: 'mdi-book-education',
          to: '/dashboard/gtu-admin/degree-programs'
        },
        {
          title: 'Subjects',
          icon: 'mdi-book-open-variant',
          to: '/dashboard/gtu-admin/subjects'
        }
      ]
    case 'DTE_ADMIN':
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
    case 'ADMIN':
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
    case 'PRINCIPAL':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/principal'
        }
      ]
    case 'HOD':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/hod'
        }
      ]
    case 'FACULTY':
      return [
        {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
          to: '/dashboard/faculty'
        }
      ]
    case 'STUDENT':
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
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'DTE Admin Portal',
      navigationItems: getNavItems('DTE_ADMIN')
    },
    meta: { requiresAuth: true, roles: ['DTE_ADMIN'] },
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
  // GTU Admin routes
  {
    path: '/dashboard/gtu-admin',
    component: () => import('@/layouts/DashboardLayout.vue'),
    props: {
      title: 'GTU Admin Portal',
      navigationItems: getNavItems('GTU_ADMIN')
    },
    meta: { requiresAuth: true, roles: ['GTU_ADMIN'] },
    children: [
      {
        path: '',
        name: 'GTUAdminDashboard',
        component: () => import('@/views/dashboards/GTUAdminDashboard.vue'),
        meta: { requiresAuth: true, roles: ['GTU_ADMIN'] }
      },
      {
        path: 'departments',
        name: 'GTUAdminDepartments',
        component: () => import('@/views/gtu-admin/DepartmentList.vue'),
        meta: { requiresAuth: true, roles: ['GTU_ADMIN'] }
      },
      {
        path: 'degree-levels',
        name: 'GTUAdminDegreeLevels',
        component: () => import('@/views/gtu-admin/DegreeLevelList.vue'),
        meta: { requiresAuth: true, roles: ['GTU_ADMIN'] }
      },
      {
        path: 'degree-programs',
        name: 'GTUAdminDegreePrograms',
        component: () => import('@/views/gtu-admin/DegreeProgramList.vue'),
        meta: { requiresAuth: true, roles: ['GTU_ADMIN'] }
      },
      {
        path: 'subjects',
        name: 'GTUAdminSubjects',
        component: () => import('@/views/gtu-admin/SubjectList.vue'),
        meta: { requiresAuth: true, roles: ['GTU_ADMIN'] }
      }
    ]
  },
  // Admin routes
  {
    path: '/dashboard/admin',
    component: () => import('@/layouts/AdminDashboardLayout.vue'),
    meta: { requiresAuth: true, role: 'ADMIN' },
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
      navigationItems: getNavItems('FACULTY')
    },
    children: [
      {
        path: '',
        name: 'FacultyDashboard',
        component: () => import('@/views/dashboards/FacultyDashboard.vue'),
        meta: { requiresAuth: true, role: 'FACULTY' }
      }
    ]
  },
  {
    path: '/dashboard/student',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'Student Portal',
      navigationItems: getNavItems('STUDENT')
    },
    children: [
      {
        path: '',
        name: 'StudentDashboard',
        component: () => import('@/views/dashboards/StudentDashboard.vue'),
        meta: { requiresAuth: true, role: 'STUDENT' }
      }
    ]
  },
  {
    path: '/dashboard/hod',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'HOD Portal',
      navigationItems: getNavItems('HOD')
    },
    children: [
      {
        path: '',
        name: 'HODDashboard',
        component: () => import('@/views/dashboards/HODDashboard.vue'),
        meta: { requiresAuth: true, role: 'HOD' }
      }
    ]
  },
  {
    path: '/dashboard/principal',
    component: () => import('@/layouts/BaseDashboardLayout.vue'),
    props: {
      title: 'Principal Portal',
      navigationItems: getNavItems('PRINCIPAL')
    },
    children: [
      {
        path: '',
        name: 'PrincipalDashboard',
        component: () => import('@/views/dashboards/PrincipalDashboard.vue'),
        meta: { requiresAuth: true, role: 'PRINCIPAL' }
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
  
  // For debugging
  console.log('Route meta:', to.meta)
  console.log('User role:', authStore.userRole)
  console.log('Is authenticated:', authStore.isAuthenticated)
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    console.log('Not authenticated, redirecting to login')
    next('/login')
  } else if (to.meta.role && !authStore.hasRole(to.meta.role)) {
    console.log('Wrong role, redirecting to default route')
    next(authStore.defaultRoute)
  } else if (to.meta.roles && !authStore.hasAnyRole(to.meta.roles)) {
    console.log('Wrong roles, redirecting to default route')
    next(authStore.defaultRoute)
  } else {
    console.log('Navigation allowed')
    next()
  }
})

export default router
