<template>
  <Scatter :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { Scatter } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from 'chart.js'
import { defineProps } from 'vue'

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend)

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartOptions: {
    type: Object,
    default: () => ({
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
  }
})
</script>
