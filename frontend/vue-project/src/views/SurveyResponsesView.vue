<template>
  <div>
    <div class="page-header">
      <div class="filter-bar">
        <input type="text" v-model="searchQuery" placeholder="Search by student or mood comment..." class="search-input">
      </div>
      <button @click="openAddModal" class="btn-primary">Add New Response</button>
    </div>

    <div class="table-container card">
      <div v-if="paginatedResponses.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('student_name')" class="sortable">
                Student Name <span v-if="sortKey === 'student_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('module_title')" class="sortable">
                Module <span v-if="sortKey === 'module_title'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('week_number')" class="sortable">
                Week <span v-if="sortKey === 'week_number'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('stress_level')" class="sortable">
                Stress Level <span v-if="sortKey === 'stress_level'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('hours_slept')" class="sortable">
                Hours Slept <span v-if="sortKey === 'hours_slept'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th>Mood Comment</th>
              <th class="actions-header">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="response in paginatedResponses" :key="response.id">
              <td>{{ response.student_name }}</td>
              <td>{{ response.module_title }}</td>
              <td>{{ response.week_number }}</td>
              <td>{{ response.stress_level }}</td>
              <td>{{ response.hours_slept }}</td>
              <td>{{ response.mood_comment }}</td>
              <td class="action-buttons">
                <button @click="openEditModal(response)" class="btn-secondary btn-sm">Edit</button>
                <button @click="handleDeleteResponse(response.id!)" class="btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No survey responses match your criteria.</p>
    </div>

    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
    </div>

    <!-- Survey Response Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3>{{ isEditMode ? 'Edit Survey Response' : 'Add New Survey Response' }}</h3>
        <form @submit.prevent="handleSaveResponse">
          <div class="form-group">
            <label for="student_id">Student ID:</label>
            <input type="number" id="student_id" v-model="currentResponse.student_id" required />
          </div>
          <div class="form-group">
            <label for="module_id">Module ID:</label>
            <input type="number" id="module_id" v-model="currentResponse.module_id" required />
          </div>
          <div class="form-group">
            <label for="week_number">Week Number:</label>
            <input type="number" id="week_number" v-model="currentResponse.week_number" required />
          </div>
          <div class="form-group">
            <label for="stress_level">Stress Level (1-5):</label>
            <input type="number" id="stress_level" v-model="currentResponse.stress_level" min="1" max="5" required />
          </div>
          <div class="form-group">
            <label for="hours_slept">Hours Slept:</label>
            <input type="number" id="hours_slept" v-model="currentResponse.hours_slept" />
          </div>
          <div class="form-group">
            <label for="mood_comment">Mood Comment:</label>
            <textarea id="mood_comment" v-model="currentResponse.mood_comment"></textarea>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn-primary">Save</button>
            <button type="button" @click="showModal = false" class="btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getSurveyResponses, addSurveyResponse, updateSurveyResponse, deleteSurveyResponse, type SurveyResponse } from '@/api/surveyResponseService'

const allResponses = ref<SurveyResponse[]>([])
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')
const searchQuery = ref('')
const sortKey = ref<keyof SurveyResponse>('student_name')
const sortOrder = ref<'asc' | 'desc'>('asc')
const currentPage = ref(1)
const itemsPerPage = ref(10)

const filteredAndSortedResponses = computed(() => {
  let responses = [...allResponses.value]
  if (searchQuery.value) {
    const lowerQuery = searchQuery.value.toLowerCase()
    responses = responses.filter(r =>
      (r.student_name && r.student_name.toLowerCase().includes(lowerQuery)) ||
      (r.mood_comment && r.mood_comment.toLowerCase().includes(lowerQuery))
    )
  }
  responses.sort((a, b) => {
    const valA = a[sortKey.value]
    const valB = b[sortKey.value]
    if (valA === undefined || valB === undefined) return 0
    let comparison = 0;
    if (valA > valB) comparison = 1;
    else if (valA < valB) comparison = -1;
    return sortOrder.value === 'asc' ? comparison : -comparison;
  })
  return responses
})

const totalPages = computed(() => {
  return Math.ceil(filteredAndSortedResponses.value.length / itemsPerPage.value)
})

const paginatedResponses = computed(() => {
  if (totalPages.value > 0 && currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedResponses.value.slice(start, end)
})

const fetchResponses = async () => {
  try {
    const response = await getSurveyResponses()
    allResponses.value = response.data
  } catch (error: any) {
    console.error('Failed to fetch survey responses:', error)
  }
}

const sortBy = (key: keyof SurveyResponse) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

onMounted(fetchResponses)

// Modal logic
const showModal = ref(false)
const isEditMode = ref(false)
const currentResponse = ref<Partial<SurveyResponse>>({ student_id: undefined, module_id: undefined, week_number: undefined, stress_level: undefined, hours_slept: undefined, mood_comment: '' })

const openAddModal = () => {
  isEditMode.value = false;
  currentResponse.value = { student_id: undefined, module_id: undefined, week_number: undefined, stress_level: undefined, hours_slept: undefined, mood_comment: '' };
  showModal.value = true;
};

const openEditModal = (response: SurveyResponse) => {
  isEditMode.value = true;
  currentResponse.value = { ...response };
  showModal.value = true;
};

const handleSaveResponse = async () => {
  try {
    if (isEditMode.value) {
      if (currentResponse.value.id) {
        await updateSurveyResponse(currentResponse.value.id, currentResponse.value as SurveyResponse);
        showMessage('Response updated successfully!', 'success');
      } else {
        showMessage('Error: Response ID is missing for update.', 'error');
      }
    } else {
      await addSurveyResponse(currentResponse.value as SurveyResponse);
      showMessage('Response added successfully!', 'success');
    }
    showModal.value = false;
    await fetchResponses();
  } catch (error: any) {
    console.error('Failed to save response:', error);
    showMessage('Failed to save response.', 'error');
  }
};

const handleDeleteResponse = async (id: number) => {
  if (confirm('Are you sure you want to delete this response?')) {
    try {
      await deleteSurveyResponse(id);
      showMessage('Response deleted successfully!', 'success');
      await fetchResponses();
    } catch (error: any) {
      console.error('Failed to delete response:', error);
      showMessage('Failed to delete response.', 'error');
    }
  }
};

const showMessage = (msg: string, type: 'success' | 'error') => {
  message.value = msg;
  messageType.value = type;
  setTimeout(() => {
    message.value = '';
    messageType.value = '';
  }, 3000);
};
</script>

<style scoped>
/* Using the same styles as StudentsView.vue for consistency */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filter-bar {
  display: flex;
  gap: 1rem;
}

.search-input, .filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input {
  width: 300px;
}

.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: var(--vt-c-indigo);
  box-shadow: 0 0 0 3px rgba(var(--vt-c-indigo-rgb), 0.2);
}

.table-container {
  background-color: var(--color-background);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border);
  padding: 0;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem 1.5rem;
  text-align: left;
  vertical-align: middle;
}

thead tr {
  border-bottom: 1px solid var(--color-border-hover);
}

th {
  font-weight: 600;
  color: var(--color-text-light);
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}

th.sortable {
  cursor: pointer;
  transition: color 0.2s;
}

th.sortable:hover {
  color: var(--color-heading);
}

th.sortable span {
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

th.actions-header {
  text-align: right;
}

tbody tr {
  border-bottom: 1px solid var(--color-border);
}

tbody tr:last-child {
  border-bottom: none;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-sm {
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
}

.no-data-message {
  text-align: center;
  padding: 4rem;
  color: var(--color-text-light);
  font-size: 1.1rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  color: var(--color-text-light);
  font-size: 0.9rem;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--color-background);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  position: relative;
}

.modal-content h3 {
  margin-top: 0;
  color: var(--color-heading);
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-text);
  font-weight: 500;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="number"],
.form-group textarea {
  width: calc(100% - 20px); /* Adjust for padding */
  padding: 0.75rem 10px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--vt-c-indigo);
  box-shadow: 0 0 0 3px rgba(var(--vt-c-indigo-rgb), 0.2);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary, .btn-secondary, .btn-danger {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}

.btn-primary:hover {
  background-color: var(--vt-c-indigo-dark);
  border-color: var(--vt-c-indigo-dark);
}

.btn-secondary:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn-danger:hover {
  background-color: #e74c3c;
  border-color: #e74c3c;
}

.message-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  color: white;
  z-index: 1001;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.message-success {
  background-color: #28a745;
}

.message-error {
  background-color: #dc3545;
}
</style>
