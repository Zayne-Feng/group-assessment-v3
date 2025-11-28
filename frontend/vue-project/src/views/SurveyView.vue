<template>
  <div class="survey-page-content">
    <h1 class="page-title-main">Submit Wellbeing Survey</h1>
    <p class="page-description">Please fill out the weekly survey to help us monitor your wellbeing and academic progress.</p>

    <form @submit.prevent="submitSurvey" class="survey-form card">
      <div class="form-grid">
        <div class="form-group">
          <label for="studentId">Student</label>
          <select id="studentId" v-model="surveyForm.student_id" required>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.full_name }} ({{ student.student_number }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="moduleId">Module (Optional)</label>
          <select id="moduleId" v-model="surveyForm.module_id">
            <option :value="null">-- Select Module --</option>
            <option v-for="module in modules" :key="module.id" :value="module.id">
              {{ module.module_title }} ({{ module.module_code }})
            </option>
          </select>
        </div>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label for="weekNumber">Week Number</label>
          <input id="weekNumber" type="number" v-model="surveyForm.week_number" required min="1">
        </div>
        <div class="form-group">
          <label for="hoursSlept">Hours Slept</label>
          <input id="hoursSlept" type="number" step="0.1" v-model="surveyForm.hours_slept" required min="0" max="24">
        </div>
      </div>

      <div class="form-group">
        <label for="stressLevel">Stress Level (1-5): <span class="stress-value">{{ surveyForm.stress_level }}</span></label>
        <input id="stressLevel" type="range" min="1" max="5" v-model="surveyForm.stress_level" required>
      </div>

      <div class="form-group">
        <label for="moodComment">Mood Comment (Optional)</label>
        <textarea id="moodComment" v-model="surveyForm.mood_comment" rows="4" placeholder="Any additional comments about your mood or wellbeing..."></textarea>
      </div>

      <button type="submit" class="btn-primary submit-button">Submit Survey</button>
    </form>
    <div v-if="message" :class="['message', messageType]">{{ message }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { submitSurvey as apiSubmitSurvey, type SurveyResponse } from '@/api/surveyService'
import { getStudents, type Student } from '@/api/studentService'
import { getModules, type Module } from '@/api/moduleService'

const authStore = useAuthStore()

const surveyForm = ref<Partial<SurveyResponse>>({
  student_id: null,
  module_id: null,
  week_number: null,
  stress_level: 3, // Default to middle
  hours_slept: 7.5, // Default
  mood_comment: ''
})

const students = ref<Student[]>([])
const modules = ref<Module[]>([])

const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

const fetchStudentsAndModulesForDropdowns = async () => {
  try {
    const [studentRes, moduleRes] = await Promise.all([getStudents(), getModules()])
    students.value = studentRes.data
    modules.value = moduleRes.data
    // Set default student_id if available
    if (students.value.length > 0) {
      surveyForm.value.student_id = students.value[0].id;
    }
  } catch (error: any) {
    console.error('Failed to fetch students or modules for dropdowns:', error)
  }
}

const submitSurvey = async () => {
  message.value = ''
  messageType.value = ''
  try {
    await apiSubmitSurvey(surveyForm.value as SurveyResponse)
    message.value = 'Survey submitted successfully!'
    messageType.value = 'success'
    // Optionally reset form
    surveyForm.value = {
      student_id: students.value.length ? students.value[0].id : null,
      module_id: null,
      week_number: null,
      stress_level: 3,
      hours_slept: 7.5,
      mood_comment: ''
    }
  } catch (error: any) {
    console.error('Failed to submit survey:', error)
    message.value = error.response?.data?.message || 'Failed to submit survey.'
    messageType.value = 'error'
  }
}

onMounted(fetchStudentsAndModulesForDropdowns)
</script>

<style scoped>
.survey-page-content {
  max-width: 700px; /* Adjusted max-width for survey form */
  margin: 0 auto; /* Center the content within main-content padding */
}

.page-title-main {
  text-align: center;
  margin-bottom: 1rem;
  color: var(--color-heading);
  font-size: 2.2rem;
  font-weight: 700;
}

.page-description {
  text-align: center;
  margin-bottom: 2.5rem;
  color: var(--color-text-light);
  font-size: 1.1rem;
}

.survey-form {
  background-color: var(--color-background);
  padding: 2.5rem 3rem;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--color-border);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.6rem;
  font-weight: 600;
  color: var(--color-text);
  font-size: 1rem;
}

.form-group input[type="number"],
.form-group input[type="text"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--vt-c-indigo);
  box-shadow: 0 0 0 3px rgba(var(--vt-c-indigo-rgb), 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group input[type="range"] {
  width: 100%;
  -webkit-appearance: none; /* Remove default styling */
  height: 8px;
  background: var(--color-border);
  border-radius: 5px;
  outline: none;
  opacity: 0.7;
  transition: opacity .2s;
}

.form-group input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--vt-c-indigo);
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.form-group input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--vt-c-indigo);
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.stress-value {
  font-weight: 700;
  color: var(--vt-c-indigo);
  margin-left: 0.5rem;
}

.submit-button {
  width: auto;
  min-width: 150px;
  padding: 0.9rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  display: block;
  margin: 2.5rem auto 0 auto; /* Center the button */
  border-radius: 8px;
  background-color: var(--vt-c-indigo);
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.submit-button:hover {
  background-color: #5c6bc0; /* Slightly lighter indigo */
  transform: translateY(-2px);
}

.message {
  text-align: center;
  margin-top: 2rem;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 500;
}

.message.success {
  background-color: rgba(16, 185, 129, 0.15);
  color: #047857;
}

.message.error {
  background-color: rgba(239, 68, 68, 0.15);
  color: #b91c1c;
}
</style>
