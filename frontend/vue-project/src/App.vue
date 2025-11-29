<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const handleLogout = () => {
  authStore.clearToken()
  router.push('/')
}

const currentPageTitle = computed(() => {
  return route.meta.title || 'Dashboard'
})
</script>

<template>
  <div class="app-shell" :class="{ 'full-width-layout': !authStore.isAuthenticated }">
    <!-- Sidebar Navigation (only shown if authenticated) -->
    <aside class="sidebar" v-if="authStore.isAuthenticated">
      <div class="sidebar-header">
        <h1 class="logo">Wellbeing</h1>
      </div>
      <nav class="main-nav">
        <RouterLink to="/dashboard"><span class="icon">📊</span> Dashboard</RouterLink>
        <RouterLink to="/students"><span class="icon">👥</span> Students</RouterLink>
        <RouterLink to="/modules" v-if="authStore.isAdmin || authStore.isCourseDirector"><span class="icon">📚</span> Modules</RouterLink>
        <RouterLink to="/alerts" v-if="authStore.isAdmin || authStore.isWellbeingOfficer"><span class="icon">🔔</span> Alerts</RouterLink>
        <RouterLink to="/users" v-if="authStore.isAdmin"><span class="icon">👤</span> Users</RouterLink>
        <RouterLink to="/enrolments" v-if="authStore.isAdmin || authStore.isCourseDirector"><span class="icon">📝</span> Enrolments</RouterLink>
        <RouterLink to="/attendance" v-if="authStore.isAdmin || authStore.isCourseDirector"><span class="icon">✅</span> Attendance</RouterLink>
        <RouterLink to="/submissions" v-if="authStore.isAdmin || authStore.isCourseDirector"><span class="icon">📬</span> Submissions</RouterLink>
        <RouterLink to="/grades" v-if="authStore.isAdmin || authStore.isCourseDirector"><span class="icon">🎓</span> Grades</RouterLink>
        <RouterLink to="/survey-responses" v-if="authStore.isAdmin || authStore.isWellbeingOfficer"><span class="icon">📝</span> Survey Responses</RouterLink>
        <RouterLink to="/survey"><span class="icon">📋</span> Submit Survey</RouterLink>
        <RouterLink to="/analytics"><span class="icon">📈</span> Analytics</RouterLink>
      </nav>
    </aside>

    <div class="main-wrapper">
      <!-- Top Bar (only shown if authenticated) -->
      <header class="top-bar" v-if="authStore.isAuthenticated">
        <h2 class="page-title">{{ currentPageTitle }}</h2>
        <div class="user-menu">
          <span class="user-name">{{ authStore.userRole }}</span>
          <div class="user-avatar"></div>
          <button @click="handleLogout" class="logout-button-top">Logout</button>
        </div>
      </header>

      <!-- Main Content Area -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  height: 100vh;
  background-color: var(--color-background-soft);
}

.sidebar {
  width: 260px;
  flex-shrink: 0;
  background-color: var(--color-background);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.sidebar-header {
  padding: 1.5rem;
  text-align: center;
  border-bottom: 1px solid var(--color-border);
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--vt-c-indigo);
}

.main-nav {
  flex-grow: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.main-nav a {
  display: flex;
  align-items: center;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  color: var(--color-text);
  font-weight: 500;
  transition: background-color 0.2s, color 0.2s;
}

.main-nav a:hover {
  background-color: var(--color-background-mute);
}

.main-nav a.router-link-exact-active {
  background-color: var(--vt-c-indigo);
  color: white;
  font-weight: 600;
}

.icon {
  margin-right: 1rem;
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.main-wrapper {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  position: relative; /* Needed for correct stacking */
  height: 100vh; /* Ensure wrapper takes full height */
}

.top-bar {
  height: 70px;
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  width: 100%;
  position: absolute; /* Take it out of flow */
  top: 0;
  left: 0;
  z-index: 10;
}

.main-content {
  flex-grow: 1;
  padding: 2rem;
  padding-top: calc(70px + 2rem); /* Add top padding equal to top-bar height + desired content padding */
  overflow-y: auto;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  font-weight: 600;
  color: var(--color-text);
  text-transform: capitalize;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--vt-c-indigo);
}

.logout-button-top {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  background: none;
  color: var(--color-text);
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.logout-button-top:hover {
  background-color: #fbe9e7;
  color: #d32f2f;
  border-color: #fbe9e7;
}

/* Styles for when user is not authenticated */
.full-width-layout .main-wrapper {
  width: 100%;
}

.full-width-layout .main-content {
  padding: 0; /* Remove padding for login/register pages */
  padding-top: 0; /* Override the padding-top */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
