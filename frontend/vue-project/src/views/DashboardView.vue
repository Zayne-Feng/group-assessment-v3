<template>
  <div> <!-- The root element is now a simple div -->
    <div class="summary-cards">
      <div class="summary-card">
        <h3>Total Students</h3>
        <p class="summary-value">{{ summary.total_students }}</p>
      </div>
      <div class="summary-card">
        <h3>Total Modules</h3>
        <p class="summary-value">{{ summary.total_modules }}</p>
      </div>
      <div class="summary-card">
        <h3>Total Users</h3>
        <p class="summary-value">{{ summary.total_users }}</p>
      </div>
      <div class="summary-card">
        <h3>Pending Alerts</h3>
        <p class="summary-value">{{ summary.pending_alerts_count }}</p>
      </div>
    </div>

    <div class="dashboard-sections">
      <router-link to="/students" class="dashboard-card">
        <h2>Student Management</h2>
        <p>View and manage student profiles, details, and academic records.</p>
      </router-link>

      <router-link to="/modules" class="dashboard-card">
        <h2>Course Management</h2>
        <p>Manage course modules, update details, and assign to students.</p>
      </router-link>

      <router-link to="/alerts" class="dashboard-card">
        <h2>Alerts & Warnings</h2>
        <p>Monitor student wellbeing alerts and manage interventions.</p>
      </router-link>
    </div>

    <div class="charts-section">
      <h2>System-wide Analytics</h2>
      <div class="charts-grid">
        <div class="chart-card">
          <h3>Overall Grade Distribution</h3>
          <DoughnutChart v-if="gradeDistributionData.labels.length" :chart-data="gradeDistributionChartData" :chart-options="doughnutChartOptions" />
          <p v-else class="no-data">No grade distribution data available.</p>
        </div>
        <div class="chart-card">
          <h3>Stress vs. Grade Correlation</h3>
          <ScatterChart v-if="stressGradeCorrelationData.datasets && stressGradeCorrelationData.datasets[0] && stressGradeCorrelationData.datasets[0].data.length" :chart-data="stressGradeCorrelationChartData" :chart-options="scatterChartOptions" />
          <p v-else class="no-data">No stress-grade correlation data available.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import DoughnutChart from '@/components/DoughnutChart.vue'
import ScatterChart from '@/components/ScatterChart.vue'
import { getDashboardSummary, getGradeDistribution, getStressGradeCorrelation } from '@/api/analyticsService'
import type { DashboardSummary, GradeDistribution, StressGradeCorrelation } from '@/api/analyticsService'

interface DashboardSummaryExtended extends DashboardSummary {
  total_users: number;
}

const summary = ref<DashboardSummaryExtended>({
  total_students: 0,
  total_modules: 0,
  pending_alerts_count: 0,
  total_users: 0
})
const gradeDistributionData = ref<GradeDistribution>({ labels: [], data: [] })
const stressGradeCorrelationData = ref<{ labels: string[]; datasets: { data: any[] }[] }>({ labels: [], datasets: [{ data: [] }] })

const gradeDistributionChartData = computed(() => ({
  labels: gradeDistributionData.value.labels,
  datasets: [
    {
      backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#DD1B16', '#F87979'],
      data: gradeDistributionData.value.data,
    },
  ],
}))

const stressGradeCorrelationChartData = computed(() => ({
  labels: stressGradeCorrelationData.value.labels,
  datasets: [
    {
      label: 'Student Data',
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      data: stressGradeCorrelationData.value.datasets[0].data,
    },
  ],
}))

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

const scatterChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      type: 'linear',
      position: 'bottom',
      title: {
        display: true,
        text: 'Average Stress Level (1-5)'
      }
    },
    y: {
      type: 'linear',
      position: 'left',
      title: {
        display: true,
        text: 'Average Grade (%)'
      }
    }
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: function(context: any) {
          const label = context.dataset.label || '';
          if (context.raw.name) {
            return `${context.raw.name}: Stress ${context.raw.x}, Grade ${context.raw.y}`;
          }
          return `${label}: Stress ${context.raw.x}, Grade ${context.raw.y}`;
        }
      }
    }
  }
})

onMounted(async () => {
  try {
    const summaryRes = await getDashboardSummary();
    summary.value = summaryRes.data as DashboardSummaryExtended;

    const gradeRes = await getGradeDistribution();
    gradeDistributionData.value = gradeRes.data;

    const correlationRes = await getStressGradeCorrelation();
    stressGradeCorrelationData.value = {
      labels: correlationRes.data.labels,
      datasets: [{
        label: 'Student Data',
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        data: correlationRes.data.data
      }]
    };

  } catch (error) {
    console.error('Failed to fetch dashboard analytics:', error);
  }
});
</script>

<style scoped>
/* Removed .dashboard-container and .dashboard-header as App.vue now handles the main layout */

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.summary-card {
  background-color: var(--color-background);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.summary-card h3 {
  color: var(--color-text);
  margin-bottom: 1rem;
  font-size: 1rem;
  font-weight: 600;
}

.summary-card .summary-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--vt-c-indigo);
}

.dashboard-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.dashboard-card {
  display: block;
  background-color: var(--color-background);
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.dashboard-card h2 {
  color: var(--vt-c-indigo);
  margin-bottom: 0.75rem;
  font-size: 1.5rem;
}

.dashboard-card p {
  color: var(--color-text-light);
  font-size: 0.9rem;
  text-align: left;
}

.charts-section h2 {
  text-align: center;
  color: var(--color-heading);
  margin-bottom: 2rem;
  font-size: 1.8rem;
  font-weight: 600;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background-color: var(--color-background);
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  height: 400px;
  display: flex;
  flex-direction: column;
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
  font-size: 1rem;
  margin: auto;
}
</style>
