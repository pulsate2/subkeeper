import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('auth_token'))
  const isAuthenticated = computed(() => !!token.value)

  // Set up axios interceptor
  const setupAxiosInterceptor = () => {
    axios.interceptors.request.use(
      (config) => {
        if (token.value) {
          config.headers.Authorization = `Bearer ${token.value}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          logout()
        }
        return Promise.reject(error)
      }
    )
  }

  const login = async (password) => {
    try {
      const response = await axios.post('/api/auth/login', { password })
      token.value = response.data.access_token
      localStorage.setItem('auth_token', token.value)
      setupAxiosInterceptor()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const logout = () => {
    token.value = null
    localStorage.removeItem('auth_token')
    delete axios.defaults.headers.common['Authorization']
  }

  const verifyToken = async () => {
    if (!token.value) return false
    
    try {
      await axios.get('/api/auth/verify')
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  // Initialize interceptor if token exists
  if (token.value) {
    setupAxiosInterceptor()
  }

  return {
    token,
    isAuthenticated,
    login,
    logout,
    verifyToken,
    setupAxiosInterceptor
  }
})