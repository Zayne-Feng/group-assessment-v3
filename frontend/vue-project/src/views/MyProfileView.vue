<template>
  <div class="profile-container">
    <div v-if="loading" class="loading-message">Loading your profile...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="student" class="profile-card card">
      <div class="profile-header">
        <h2>My Profile</h2>
      </div>
      <div class="profile-body">
        <div class="profile-item">
          <span class="item-label">Full Name:</span>
          <span class="item-value">{{ student.full_name }}</span>
        </div>
        <div class="profile-item">
          <span class="item-label">Student Number:</span>
          <span class="item-value">{{ student.student_number }}</span>
        </div>
        <div class="profile-item">
          <span class="item-label">Email Address:</span>
          <span class="item-value">{{ student.email }}</span>
        </div>
        <div class="profile-item">
          <span class="item-label">Course:</span>
          <span class="item-value">{{ student.course_name || 'Not Assigned' }}</span>
        </div>
        <div class="profile-item">
          <span class="item-label">Year of Study:</span>
          <span class="item-value">{{ student.year_of_study || 'Not Assigned' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMyProfile } from '@/api/studentService'
import type { Student } from '@/api/studentService'

const student = ref<Student | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await getMyProfile()
    student.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to load profile.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
}

.profile-card {
  background-color: var(--color-background);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border);
  overflow: hidden; /* Ensures the header and body are contained within the rounded corners */
}

.profile-header {
  background-color: var(--color-background-mute);
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--color-border);
}

.profile-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: var(--color-heading);
}

.profile-body {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-label {
  font-size: 0.9rem;
  color: var(--color-text-light);
  text-transform: uppercase;
  font-weight: 600;
}

.item-value {
  font-size: 1.1rem;
  color: var(--color-text);
}

.loading-message,
.error-message {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
  color: var(--color-text-light);
}

.error-message {
  color: #ef4444; /* Red */
}
</style>
