import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/lib/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isEditor = computed(() => user.value?.role === 'editor')

  const login = async (username, password) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.login(username, password)
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      return true
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || 'Login failed'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const getCurrentUser = async () => {
    if (token.value) {
      try {
        const response = await api.getCurrentUser()
        user.value = response
      } catch (e) {
        logout()
      }
    }
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    isEditor,
    login,
    logout,
    getCurrentUser
  }
})
