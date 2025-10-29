import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import UserDashboard from '@/views/UserDashboard.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth state from localStorage
  if (!authStore.isLoggedIn && localStorage.getItem('access_token')) {
    authStore.initializeAuth()
  }

  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      next('/login')
      return
    }
    
    if (to.meta.role && authStore.role !== to.meta.role) {
      // Redirect to appropriate dashboard based on role
      if (authStore.role === 'admin') {
        next('/admin/dashboard')
      } else {
        next('/dashboard')
      }
      return
    }
  }

  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    // Redirect authenticated users to their dashboard
    if (authStore.role === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/dashboard')
    }
    return
  }

  next()
})

export default router