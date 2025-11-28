import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios' // Import axios

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth' // Import auth store

const app = createApp(App)
const pinia = createPinia() // Create pinia instance

app.use(pinia) // Use pinia instance
app.use(router)

// Configure Axios interceptor
axios.interceptors.request.use(config => {
  const authStore = useAuthStore() // Get store instance
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// Optional: Axios interceptor for handling 401 Unauthorized responses
axios.interceptors.response.use(response => response, error => {
  if (error.response && error.response.status === 401) {
    const authStore = useAuthStore()
    authStore.clearToken()
    router.push('/') // Redirect to login page
  }
  return Promise.reject(error)
})

app.mount('#app')
