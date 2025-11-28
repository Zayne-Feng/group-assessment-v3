<template>
  <div v-if="student">
    <div class="page-header">
      <h1>{{ student.full_name }} Details</h1>
    </div>

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

    <div class="charts-section card">
      <h2>Performance & Wellbeing Trends</h2>
      <div class="charts-grid">
        <div class="chart-card">
          <h3>Weekly Stress Trend</h3>
          <LineChart v-if="stressData.labels.length" :chart-data="stressChartData" :chart-options="lineChartOptions" />
          <p v-else class="no-data">No stress data available.</p>
        </div>
        <div class="chart-card">
          <h3>Weekly Attendance Trend (%)</h3>
          <BarChart v-if="attendanceData.labels.length" :chart-data="attendanceChartData" :chart-options="barChartOptions" />
          <p v-else class="no-data">No attendance data available.</p>
        </div>
      </div>
    </div>

    <div class="student-alerts-section card">
      <h2>Alert History</h2>
      <div v-if="paginatedAlerts.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('week_number')" class="sortable">
                Week <span v-if="sortKey === 'week_number'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('reason')" class="sortable">
                Reason <span v-if="sortKey === 'reason'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('created_at')" class="sortable">
                Created At <span v-if="sortKey === 'created_at'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('resolved')" class="sortable">
                Status <span v-if="sortKey === 'resolved'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="alert in paginatedAlerts" :key="alert.id">
              <td>{{ alert.week_number }}</td>
              <td>{{ alert.reason }}</td>
              <td>{{ new Date(alert.created_at).toLocaleDateString() }}</td>
              <td>
                <span :class="['status-badge', alert.resolved ? 'status-success' : 'status-danger']">
                  {{ alert.resolved ? 'Resolved' : 'Pending' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No alert history for this student.</p>

      <div class="pagination-controls" v-if="allAlerts.length > itemsPerPage">
        <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
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
import { getStudentById, type Student } from '@/api/studentService'
import { getStressTrendForStudent, getAttendanceTrendForStudent, type TrendData } from '@/api/analyticsService' // Corrected import
import { getAlertsByStudentId, type Alert } from '@/api/alertService'
import LineChart from '@/components/LineChart.vue'
import BarChart from '@/components/BarChart.vue'

const route = useRoute()
const studentId = parseInt(route.params.id as string)

const student = ref<Student | null>(null)
const stressData = ref<TrendData>({ labels: [], data: [] })
const attendanceData = ref<TrendData>({ labels: [], data: [] })
const allAlerts = ref<Alert[]>([]) // All alerts for this student

// Sorting for alerts
const sortKey = ref<keyof Alert>('created_at')
const sortOrder = ref<'asc' | 'desc'>('desc')

// Pagination for alerts
const currentPage = ref(1)
const itemsPerPage = ref(5) // Display fewer alerts per page

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

// Computed properties for alerts interactivity
const sortedAlerts = computed(() => {
  let alerts = [...allAlerts.value];
  alerts.sort((a, b) => {
    const valA = a[sortKey.value];
    const valB = b[sortKey.value];
    if (valA === undefined || valB === undefined) return 0;

    let comparison = 0;
    if (typeof valA === 'string' && typeof valB === 'string') {
      comparison = valA.localeCompare(valB);
    } else if (valA > valB) {
      comparison = 1;
    } else if (valA < valB) {
      comparison = -1;
    }
    return sortOrder.value === 'asc' ? comparison : -comparison;
  });
  return alerts;
});

const totalPages = computed(() => {
  return Math.ceil(sortedAlerts.value.length / itemsPerPage.value);
});

const paginatedAlerts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedAlerts.value.slice(start, end);
});

// Methods for alerts
const sortBy = (key: keyof Alert) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

onMounted(async () => {
  try {
    const [studentRes, stressRes, attendanceRes, alertsRes] = await Promise.all([
      getStudentById(studentId),
      getStressTrendForStudent(studentId),
      getAttendanceTrendForStudent(studentId),
      getAlertsByStudentId(studentId) // Fetch all alerts for this student
    ])

    student.value = studentRes.data
    stressData.value = stressRes.data
    attendanceData.value = attendanceRes.data
    allAlerts.value = alertsRes.data

  } catch (error) {
    console.error('Failed to fetch student data:', error)
    // Optionally set an error message for the user
  }
})
</script>

<style scoped>
/* General page container is handled by App.vue's main-content padding */

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-heading);
}

.detail-card, .charts-section, .student-alerts-section {
  background-color: var(--color-background);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border);
  margin-bottom: 2rem; /* Spacing between sections */
}

.detail-card h2, .charts-section h2, .student-alerts-section h2 {
  color: var(--vt-c-indigo);
  margin-bottom: 1.5rem;
  font-size: 1.6rem;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.75rem;
}

.detail-card p {
  margin-bottom: 0.75rem;
  color: var(--color-text);
}

.detail-card strong {
  color: var(--color-heading);
}

.detail-card h3 {
  color: var(--color-heading);
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-size: 1.3rem;
  font-weight: 600;
}

.detail-card ul {
  list-style: none; /* Remove default bullet */
  padding-left: 0;
  margin-top: 0.5rem;
}

.detail-card ul li {
  background-color: var(--color-background-soft);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  display: inline-block; /* Display as tags */
  margin-right: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text);
}

.charts-section {
  margin-top: 2rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1.5rem; /* Adjust padding for chart cards */
}

.chart-card h3 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--color-heading);
  font-size: 1.2rem;
  font-weight: 600;
}

.no-data {
  text-align: center;
  color: var(--color-text-light);
  padding: 2rem;
  font-size: 1.1rem;
  margin: auto;
}

.loading-message {
  text-align: center;
  padding: 4rem;
  color: var(--color-text);
  font-size: 1.2rem;
}

/* Table styles for alerts history */
.student-alerts-section .table-responsive {
  overflow-x: auto;
}

.student-alerts-section table {
  width: 100%;
  border-collapse: collapse;
}

.student-alerts-section th, .student-alerts-section td {
  padding: 1rem 1.5rem;
  text-align: left;
  vertical-align: middle;
}

.student-alerts-section thead tr {
  border-bottom: 1px solid var(--color-border-hover);
}

.student-alerts-section th {
  font-weight: 600;
  color: var(--color-text-light);
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
  cursor: pointer; /* Make sortable */
  transition: color 0.2s;
}

.student-alerts-section th:hover {
  color: var(--color-heading);
}

.student-alerts-section th span {
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.student-alerts-section tbody tr {
  border-bottom: 1px solid var(--color-border);
}

.student-alerts-section tbody tr:last-child {
  border-bottom: none;
}

.status-badge {
  display: inline-block;
  padding: 0.3em 0.7em;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-success {
  background-color: #10b981;
}

.status-danger {
  background-color: #ef4444;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.page-info {
  color: var(--color-text-light);
  font-size: 0.9rem;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
