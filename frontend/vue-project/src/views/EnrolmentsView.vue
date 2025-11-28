<template>
  <div>
    <div class="page-header">
      <div class="filter-bar">
        <input type="text" v-model="searchQuery" placeholder="Search by student or module..." class="search-input">
        <select v-model="selectedModule" class="filter-select">
          <option value="">All Modules</option>
          <option v-for="module in modules" :key="module.id" :value="module.module_title">{{ module.module_title }}</option>
        </select>
      </div>
      <button @click="openAddModal" v-if="authStore.isAdmin" class="btn-primary">Add New Enrolment</button>
    </div>

    <div class="table-container card">
      <div v-if="paginatedEnrolments.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('student_name')" class="sortable">
                Student Name <span v-if="sortKey === 'student_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('module_title')" class="sortable">
                Module Title <span v-if="sortKey === 'module_title'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('enrol_date')" class="sortable">
                Enrol Date <span v-if="sortKey === 'enrol_date'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="actions-header" v-if="authStore.isAdmin">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="enrolment in paginatedEnrolments" :key="enrolment.id">
              <td>{{ enrolment.student_name }}</td>
              <td>{{ enrolment.module_title }}</td>
              <td>{{ enrolment.enrol_date }}</td>
              <td class="action-buttons" v-if="authStore.isAdmin">
                <button @click="openEditModal(enrolment)" class="btn-secondary btn-sm">Edit</button>
                <button @click="deleteEnrolment(enrolment.id!)" class="btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No enrolments match your criteria.</p>
    </div>

    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
    </div>

    <!-- Add/Edit Enrolment Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>{{ isEditMode ? 'Edit Enrolment' : 'Add Enrolment' }}</h2>
        <form @submit.prevent="saveEnrolment" class="modal-form">
          <div class="form-group">
            <label for="studentId">Student</label>
            <select id="studentId" v-model="currentEnrolment.student_id" required>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.full_name }} ({{ student.student_number }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="moduleId">Module</label>
            <select id="moduleId" v-model="currentEnrolment.module_id" required>
              <option v-for="module in modules" :key="module.id" :value="module.id">
                {{ module.module_title }} ({{ module.module_code }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="enrolDate">Enrol Date</label>
            <input id="enrolDate" type="date" v-model="currentEnrolment.enrol_date">
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn-primary">Save</button>
            <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
          </div>
        </form>
        <div v-if="message" :class="['message', messageType]">{{ message }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getEnrolments, addEnrolment, updateEnrolment, deleteEnrolment, type Enrolment } from '@/api/enrolmentService'
import { getStudents, type Student } from '@/api/studentService'
import { getModules, type Module } from '@/api/moduleService'

const authStore = useAuthStore()

// Data
const allEnrolments = ref<Enrolment[]>([])
const students = ref<Student[]>([]) // For dropdowns
const modules = ref<Module[]>([])   // For dropdowns
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

// Filtering and Searching
const searchQuery = ref('')
const selectedModule = ref('')

// Sorting
const sortKey = ref<keyof Enrolment>('enrol_date')
const sortOrder = ref<'asc' | 'desc'>('desc') // Default to newest first

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Computed properties for interactivity
const filteredAndSortedEnrolments = computed(() => {
  let enrolments = [...allEnrolments.value]

  // Filter by search query
  if (searchQuery.value) {
    const lowerQuery = searchQuery.value.toLowerCase()
    enrolments = enrolments.filter(e =>
      e.student_name?.toLowerCase().includes(lowerQuery) ||
      e.module_title?.toLowerCase().includes(lowerQuery)
    )
  }

  // Filter by module
  if (selectedModule.value) {
    enrolments = enrolments.filter(e => e.module_title === selectedModule.value)
  }

  // Sort
  enrolments.sort((a, b) => {
    const valA = a[sortKey.value]
    const valB = b[sortKey.value]
    if (valA === undefined || valB === undefined) return 0

    let comparison = 0;
    if (typeof valA === 'string' && typeof valB === 'string') {
      comparison = valA.localeCompare(valB);
    } else if (valA > valB) {
      comparison = 1;
    } else if (valA < valB) {
      comparison = -1;
    }
    return sortOrder.value === 'asc' ? comparison : -comparison;
  })

  return enrolments
})

const totalPages = computed(() => {
  return Math.ceil(filteredAndSortedEnrolments.value.length / itemsPerPage.value)
})

const paginatedEnrolments = computed(() => {
  if (totalPages.value > 0 && currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedEnrolments.value.slice(start, end)
})

// Methods
const fetchEnrolments = async () => {
  try {
    const response = await getEnrolments()
    allEnrolments.value = response.data
  } catch (error: any) {
    console.error('Failed to fetch enrolments:', error)
  }
}

const fetchStudentsAndModulesForDropdowns = async () => {
  try {
    const [studentRes, moduleRes] = await Promise.all([getStudents(), getModules()])
    students.value = studentRes.data
    modules.value = moduleRes.data
  } catch (error: any) {
    console.error('Failed to fetch students or modules for dropdowns:', error)
  }
}

const sortBy = (key: keyof Enrolment) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

// Modal logic
const showModal = ref(false)
const isEditMode = ref(false)
const currentEnrolment = ref<Partial<Enrolment>>({ student_id: 0, module_id: 0, enrol_date: new Date().toISOString().split('T')[0] })

const openAddModal = () => {
  isEditMode.value = false
  currentEnrolment.value = {
    student_id: students.value.length ? students.value[0].id : 0,
    module_id: modules.value.length ? modules.value[0].id : 0,
    enrol_date: new Date().toISOString().split('T')[0]
  }
  showModal.value = true
}

const openEditModal = (enrolment: Enrolment) => {
  isEditMode.value = true
  currentEnrolment.value = { ...enrolment }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  message.value = ''
  messageType.value = ''
}

const saveEnrolment = async () => {
  message.value = ''
  messageType.value = ''
  try {
    if (isEditMode.value && currentEnrolment.value.id) {
      await updateEnrolment(currentEnrolment.value.id, currentEnrolment.value as Enrolment)
      message.value = 'Enrolment updated successfully!'
      messageType.value = 'success'
    } else {
      const { id, student_name, module_title, ...newEnrolment } = currentEnrolment.value;
      await addEnrolment(newEnrolment as Enrolment)
      message.value = 'Enrolment added successfully!'
      messageType.value = 'success'
    }
    await fetchEnrolments()
    closeModal()
  } catch (error: any) {
    console.error('Failed to save enrolment:', error)
    message.value = error.response?.data?.message || 'Failed to save enrolment.'
    messageType.value = 'error'
  }
}

const deleteEnrolment = async (id: number) => {
  if (confirm('Are you sure you want to delete this enrolment? (Logical Delete)')) {
    try {
      await deleteEnrolment(id)
      message.value = 'Enrolment deleted successfully!'
      messageType.value = 'success'
      await fetchEnrolments()
    } catch (error: any) {
      console.error('Failed to delete enrolment:', error)
      message.value = error.response?.data?.message || 'Failed to delete enrolment.'
      messageType.value = 'error'
    }
  }
}

onMounted(async () => {
  await fetchStudentsAndModulesForDropdowns()
  await fetchEnrolments()
})
</script>

<style scoped>
/* Reusing StudentsView.vue styles for consistency */
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

.status-badge {
  display: inline-block;
  padding: 0.3em 0.7em;
  border-radius: 12px; /* Pill shape */
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-success {
  background-color: #10b981; /* Emerald */
}

.status-danger {
  background-color: #ef4444; /* Red */
}

/* Modal Specific Styles (from SubmissionsView.vue, adapted) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 600px; /* Adjusted width for Enrolment modal */
  background-color: var(--color-background);
  padding: 2rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
  font-size: 1.8rem;
}

.modal-form .form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Two columns for student/module selection */
  gap: 1.5rem;
}

.modal-form .form-group {
  margin-bottom: 1.5rem;
}

.modal-form .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.modal-form .form-group input[type="text"],
.modal-form .form-group input[type="date"],
.modal-form .form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.modal-form .form-group input:focus,
.modal-form .form-group select:focus {
  outline: none;
  border-color: var(--vt-c-indigo);
  box-shadow: 0 0 0 3px rgba(var(--vt-c-indigo-rgb), 0.2);
}

.form-group-checkbox {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.form-group-checkbox input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
  accent-color: var(--vt-c-indigo);
}

.form-group-checkbox label {
  font-weight: 500;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style>
