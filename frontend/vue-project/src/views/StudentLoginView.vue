<template>
  <div class="auth-split-container">
    <div class="left-panel">
      <div class="overlay-content">
        <h1>Student Wellbeing</h1>
        <p>Your space for academic and personal wellness</p>
      </div>
    </div>
    <div class="right-panel">
      <div class="form-wrapper">
        <h2>Student Login</h2>
        <p class="subtitle">Welcome, please enter your details to log in.</p>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username (Your Email)</label>
            <input id="username" type="text" v-model="username" required placeholder="Enter your email">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input id="password" type="password" v-model="password" required placeholder="Enter your password">
          </div>
          <button type="submit" class="btn-submit">Sign In</button>
        </form>
        <div v-if="message" :class="['message', messageType]">{{ message }}</div>
        <div class="switch-form">
          Don't have an account?
          <router-link to="/student/register">Register here</router-link>
        </div>
        <div class="switch-form-alt">
          <router-link to="/">Staff Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { login as apiLogin } from '@/api/authService'

const username = ref('')
const password = ref('')
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')
const authStore = useAuthStore()

const handleLogin = async () => {
  message.value = ''
  messageType.value = ''
  try {
    const response = await apiLogin({
      username: username.value,
      password: password.value,
      context: 'student' // Specify context for student login
    })

    message.value = response.data.message
    messageType.value = 'success'
    authStore.setToken(response.data.access_token)
    authStore.setUserRole(response.data.user_role)

    setTimeout(() => {
      window.location.href = '/dashboard'
    }, 100);

  } catch (error: any) {
    message.value = error.response?.data?.message || 'An unexpected error occurred.'
    messageType.value = 'error'
  }
}
</script>

<style scoped>
/* Styles are copied from LoginView.vue for consistency, with an added style for the alternate link */
.auth-split-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.left-panel {
  width: 55%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.overlay-content {
  text-align: center;
  z-index: 1;
  padding: 2rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(5px);
}

.overlay-content h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.overlay-content p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.right-panel {
  width: 45%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--color-background-soft);
  padding: 3rem;
}

.form-wrapper {
  width: 100%;
  max-width: 400px;
}

.form-wrapper h2 {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.form-wrapper .subtitle {
  font-size: 1rem;
  color: var(--color-text-light);
  margin-bottom: 2.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.form-group input {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input::placeholder {
  color: var(--color-text-light);
}

.form-group input:focus {
  outline: none;
  border-color: var(--vt-c-indigo);
  box-shadow: 0 0 0 3px rgba(var(--vt-c-indigo-rgb), 0.2);
}

.btn-submit {
  width: 100%;
  padding: 0.9rem;
  border: none;
  border-radius: 8px;
  background: linear-gradient(90deg, #e73c7e, #23a6d5);
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.3s, transform 0.2s;
  margin-top: 1rem;
}

.btn-submit:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.message {
  text-align: center;
  margin-top: 1.5rem;
  padding: 0.8rem;
  border-radius: 8px;
}

.message.success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.message.error {
  background-color: #ffebee;
  color: #c62828;
}

.switch-form {
  text-align: center;
  margin-top: 2rem;
  color: var(--color-text-light);
}

.switch-form a {
  color: var(--vt-c-indigo);
  text-decoration: none;
  font-weight: 600;
}

.switch-form a:hover {
  text-decoration: underline;
}

.switch-form-alt {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.switch-form-alt a {
  color: var(--color-text-light);
  text-decoration: none;
}

.switch-form-alt a:hover {
  text-decoration: underline;
}
</style>
