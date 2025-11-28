<template>
  <div v-if="student" class="page-container">
    <h1>{{ student.full_name }}</h1>
    <div class="detail-card card">
      <h2>Student Information</h2>
      <p><strong>Student Number:</strong> {{ student.student_number }}</p>
      <p><strong>Email:</strong> {{ student.email }}</p>
      <p><strong>Course:</strong> {{ student.course_name }}</p>
      <p><strong>Year of Study:</strong> {{ student.year_of_study }}</p>
      <h3>Enrolled Modules</h3>
      <ul v-if="student.enrolments && student.enrolments.length">
        <li v-for="module in student.enrolments" :key="module">{{ module }}</li>
      </ul>
      <p v-else class="no-data">No enrolled modules.</p>
    </div>

    <div class="charts-section">
      <h2>Student Performance & Wellbeing Trends</h2>
      <div class="charts-grid">
        <div class="chart-card card">
          <h3>Weekly Stress Trend</h3>
          <LineChart v-if="stressData.labels.length" :chart-data="stressChartData" :chart-options="lineChartOptions" />
          <p v-else class="no-data">No stress data available.</p>
        </div>
        <div class="chart-card card">
          <h3>Weekly Attendance Trend (%)</h3>
          <BarChart v-if="attendanceData.labels.length" :chart-data="attendanceChartData" :chart-options="barChartOptions" />
          <p v-else class="no-data">No attendance data available.</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="loading-message">
    <p>Loading student details...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import LineChart from '@/components/LineChart.vue'
import BarChart from '@/components/BarChart.vue'

const route = useRoute()
const studentId = route.params.id

const student = ref<any>(null)
const stressData = ref({ labels: [], data: [] })
const attendanceData = ref({ labels: [], data: [] })

const stressChartData = computed(() => ({
  labels: stressData.value.labels,
  datasets: [
    {
      label: 'Stress Level (1-5)',
      backgroundColor: 'rgba(248, 121, 121, 0.6)',
      borderColor: '#f87979',
      tension: 0.3,
      data: stressData.value.data,
    },
  ],
}))

const attendanceChartData = computed(() => ({
  labels: attendanceData.value.labels,
  datasets: [
    {
      label: 'Attendance Rate (%)',
      backgroundColor: 'rgba(66, 185, 131, 0.6)',
      borderColor: '#42b983',
      data: attendanceData.value.data,
    },
  ],
}))

const lineChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 5,
      title: {
        display: true,
        text: 'Stress Level'
      }
    }
  }
})

const barChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: 'Attendance Rate (%)'
      }
    }
  }
})

onMounted(async () => {
  try {
    const studentRes = await axios.get(`/api/analysis/students/${studentId}`)
    student.value = studentRes.data

    const stressRes = await axios.get(`/api/analysis/students/${studentId}/stress-trend`)
    stressData.value = stressRes.data

    const attendanceRes = await axios.get(`/api/analysis/students/${studentId}/attendance-trend`)
    attendanceData.value = attendanceRes.data

  } catch (error) {
    console.error('Failed to fetch student data:', error)
    // Optionally set an error message for the user
  }
})
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: var(--color-background-light);
  border-radius: var(--border-radius-base);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
  font-size: 2.2rem;
  font-weight: 700;
}

.detail-card h2, .charts-section h2 {
  color: var(--color-primary);
  margin-bottom: 1rem;
  font-size: 1.6rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.5rem;
}

.detail-card ul {
  list-style: inside;
  padding-left: 1rem;
}

.detail-card ul li {
  margin-bottom: 0.5rem;
}

.charts-section {
  margin-top: 2rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
}

.chart-card {
  height: 400px; /* Fixed height for charts */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.chart-card h3 {
  text-align: center;
  margin-bottom: 1rem;
  color: var(--color-heading);
  font-size: 1.2rem;
}

.no-data {
  text-align: center;
  color: var(--color-text-light);
  padding: 2rem;
}

.loading-message {
  text-align: center;
  padding: 4rem;
  color: var(--color-text);
}
</style>
