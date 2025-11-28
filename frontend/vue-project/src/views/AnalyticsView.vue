<template>
  <div class="page-container">
    <h1>Advanced Analytics & Reports</h1>

    <div class="charts-grid">
      <div class="chart-card card">
        <h3>Overall Attendance Rate</h3>
        <p class="summary-value">{{ overallAttendanceRate }}%</p>
        <p class="no-data" v-if="overallAttendanceRate === 0">No attendance data available.</p>
      </div>

      <div class="chart-card card">
        <h3>Submission Status Distribution</h3>
        <DoughnutChart v-if="submissionStatusData.labels.length" :chart-data="submissionStatusChartData" :chart-options="doughnutChartOptions" />
        <p v-else class="no-data">No submission data available.</p>
      </div>

      <div class="chart-card card">
        <h3>Average Stress Level by Module</h3>
        <BarChart v-if="stressByModuleData.labels.length" :chart-data="stressByModuleChartData" :chart-options="barChartOptions" />
        <p v-else class="no-data">No stress data by module available.</p>
      </div>
    </div>

    <div class="high-risk-students-section card">
      <h2>High-Risk Students</h2>
      <div v-if="highRiskStudents.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Student Name</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in highRiskStudents" :key="student.id">
              <td>
                <router-link :to="{ name: 'student-detail', params: { id: student.id } }">
                  {{ student.name }}
                </router-link>
              </td>
              <td>{{ student.reason }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No high-risk students identified.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import DoughnutChart from '@/components/DoughnutChart.vue'
import BarChart from '@/components/BarChart.vue'

const overallAttendanceRate = ref(0)
const submissionStatusData = ref({ labels: [], data: [] })
const stressByModuleData = ref({ labels: [], data: [] })
const highRiskStudents = ref([])

const doughnutChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
    },
    title: {
      display: false,
    }
  }
})

const barChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Average Stress Level'
      }
    }
  }
})

const submissionStatusChartData = computed(() => ({
  labels: submissionStatusData.value.labels,
  datasets: [
    {
      backgroundColor: ['#4CAF50', '#FFC107', '#F44336'], // Green, Amber, Red
      data: submissionStatusData.value.data,
    },
  ],
}))

const stressByModuleChartData = computed(() => ({
  labels: stressByModuleData.value.labels,
  datasets: [
    {
      label: 'Average Stress Level',
      backgroundColor: '#60a5fa', // Secondary blue
      data: stressByModuleData.value.data,
    },
  ],
}))

onMounted(async () => {
  try {
    const [
      attendanceRes,
      submissionRes,
      stressByModuleRes,
      highRiskRes
    ] = await Promise.all([
      axios.get('/api/analysis/overall-attendance-rate'),
      axios.get('/api/analysis/submission-status-distribution'),
      axios.get('/api/analysis/stress-by-module'),
      axios.get('/api/analysis/high-risk-students')
    ])

    overallAttendanceRate.value = attendanceRes.data.overall_attendance_rate
    submissionStatusData.value = submissionRes.data
    stressByModuleData.value = stressByModuleRes.data
    highRiskStudents.value = highRiskRes.data

  } catch (error) {
    console.error('Failed to fetch analytics data:', error)
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

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Adjust for more charts */
  gap: 2rem;
  margin-bottom: 3rem;
}

.chart-card {
  height: 350px; /* Consistent height for charts */
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

.summary-value {
  font-size: 3rem;
  font-weight: bold;
  color: var(--color-primary);
  margin-top: 1rem;
}

.high-risk-students-section {
  margin-top: 3rem;
}

.high-risk-students-section h2 {
  color: var(--color-primary);
  margin-bottom: 1rem;
  font-size: 1.8rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.5rem;
  text-align: center;
}

.no-data {
  text-align: center;
  color: var(--color-text-light);
  padding: 2rem;
}

.no-data-message {
  text-align: center;
  padding: 1.5rem;
  color: var(--color-text-light);
  font-style: italic;
}
</style>
