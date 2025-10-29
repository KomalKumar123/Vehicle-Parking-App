import { defineStore } from 'pinia'
import api from '@/services/api'

// JWT decode function
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (error) {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    accessToken: null,
    role: null
  }),

  getters: {
    isAdmin: (state) => state.role === 'admin',
    isUser: (state) => state.role === 'user'
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/auth/login', credentials)
        const { access_token } = response.data
        
        // Store token
        localStorage.setItem('access_token', access_token)
        this.accessToken = access_token
        
        // Decode JWT to get role
        const decoded = parseJwt(access_token)
        this.role = decoded?.role || 'user'
        this.isLoggedIn = true
        
        return response.data
      } catch (error) {
        throw error
      }
    },

    async register(userData) {
      try {
        const response = await api.post('/auth/register', userData)
        return response.data
      } catch (error) {
        throw error
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      this.isLoggedIn = false
      this.accessToken = null
      this.role = null
    },

    initializeAuth() {
      const token = localStorage.getItem('access_token')
      if (token) {
        const decoded = parseJwt(token)
        if (decoded && decoded.exp > Date.now() / 1000) {
          this.accessToken = token
          this.role = decoded.role || 'user'
          this.isLoggedIn = true
        } else {
          this.logout()
        }
      }
    }
  }
})