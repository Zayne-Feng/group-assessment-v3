import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const userRole = ref<string | null>(localStorage.getItem('user_role'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => userRole.value === 'admin')
  const isCourseDirector = computed(() => userRole.value === 'course_director')
  const isWellbeingOfficer = computed(() => userRole.value === 'wellbeing_officer')
  const isUser = computed(() => userRole.value === 'user') // For general users/students

  function setToken(token: string) {
    accessToken.value = token
    localStorage.setItem('access_token', token)
  }

  function setUserRole(role: string) {
    userRole.value = role
    localStorage.setItem('user_role', role)
  }

  function clearToken() {
    accessToken.value = null
    userRole.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_role')
  }

  return {
    accessToken,
    userRole,
    isAuthenticated,
    isAdmin,
    isCourseDirector,
    isWellbeingOfficer,
    isUser,
    setToken,
    setUserRole,
    clearToken
  }
})
