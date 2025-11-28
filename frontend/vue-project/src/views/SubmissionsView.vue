<template>
  <div>
    <div class="page-header">
      <div class="filter-bar">
        <input type="text" v-model="searchQuery" placeholder="Search by student, module or assessment..." class="search-input">
        <select v-model="selectedModule" class="filter-select">
          <option value="">All Modules</option>
          <option v-for="module in modules" :key="module.id" :value="module.module_title">{{ module.module_title }}</option>
        </select>
        <select v-model="selectedStatus" class="filter-select">
          <option value="">All Statuses</option>
          <option value="submitted">Submitted</option>
          <option value="not_submitted">Not Submitted</option>
          <option value="late">Late</option>
          <option value="on_time">On Time</option>
        </select>
      </div>
      <button @click="openAddModal" v-if="authStore.isAdmin" class="btn-primary">Add New Submission Record</button>
    </div>

    <div class="table-container card">
      <div v-if="paginatedSubmissionRecords.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('student_name')" class="sortable">
                Student Name <span v-if="sortKey === 'student_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('module_title')" class="sortable">
                Module <span v-if="sortKey === 'module_title'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('assessment_name')" class="sortable">
                Assessment <span v-if="sortKey === 'assessment_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('due_date')" class="sortable">
                Due Date <span v-if="sortKey === 'due_date'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('submitted_date')" class="sortable">
                Submitted Date <span v-if="sortKey === 'submitted_date'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('is_submitted')" class="sortable">
                Submitted <span v-if="sortKey === 'is_submitted'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('is_late')" class="sortable">
                Late <span v-if="sortKey === 'is_late'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="actions-header" v-if="authStore.isAdmin">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in paginatedSubmissionRecords" :key="record.id">
              <td>{{ record.student_name }}</td>
              <td>{{ record.module_title }}</td>
              <td>{{ record.assessment_name }}</td>
              <td>{{ record.due_date }}</td>
              <td>{{ record.submitted_date || 'N/A' }}</td>
              <td>
                <span :class="['status-badge', record.is_submitted ? 'status-success' : 'status-danger']">
                  {{ record.is_submitted ? 'Yes' : 'No' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', record.is_late ? 'status-danger' : 'status-success']">
                  {{ record.is_late ? 'Yes' : 'No' }}
                </span>
              </td>
              <td class="action-buttons" v-if="authStore.isAdmin">
                <button @click="openEditModal(record)" class="btn-secondary btn-sm">Edit</button>
                <button @click="deleteRecord(record.id!)" class="btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No submission records match your criteria.</p>
    </div>

    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
    </div>

    <!-- Add/Edit Submission Record Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>{{ isEditMode ? 'Edit Submission Record' : 'Add Submission Record' }}</h2>
        <form @submit.prevent="saveRecord" class="modal-form">
          <div class="form-grid">
            <div class="form-group">
              <label for="studentId">Student</label>
              <select id="studentId" v-model="currentRecord.student_id" required>
                <option v-for="student in students" :key="student.id" :value="student.id">
                  {{ student.full_name }} ({{ student.student_number }})
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="moduleId">Module</label>
              <select id="moduleId" v-model="currentRecord.module_id" required>
                <option v-for="module in modules" :key="module.id" :value="module.id">
                  {{ module.module_title }} ({{ module.module_code }})
                </option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label for="assessmentName">Assessment Name</label>
            <input id="assessmentName" type="text" v-model="currentRecord.assessment_name" required>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label for="dueDate">Due Date</label>
              <input id="dueDate" type="date" v-model="currentRecord.due_date" required>
            </div>
            <div class="form-group">
              <label for="submittedDate">Submitted Date</label>
              <input id="submittedDate" type="date" v-model="currentRecord.submitted_date">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group-checkbox">
              <input id="isSubmitted" type="checkbox" v-model="currentRecord.is_submitted">
              <label for="isSubmitted">Is Submitted</label>
            </div>
            <div class="form-group-checkbox">
              <input id="isLate" type="checkbox" v-model="currentRecord.is_late">
              <label for="isLate">Is Late</label>
            </div>
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
import { getSubmissionRecords, addSubmissionRecord, updateSubmissionRecord, deleteSubmissionRecord, type SubmissionRecord } from '@/api/submissionService'
import { getStudents, type Student } from '@/api/studentService'
import { getModules, type Module } from '@/api/moduleService'

const authStore = useAuthStore()

// Data
const allSubmissionRecords = ref<SubmissionRecord[]>([])
const students = ref<Student[]>([]) // For dropdowns
const modules = ref<Module[]>([])   // For dropdowns
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

// Filtering and Searching
const searchQuery = ref('')
const selectedModule = ref('')
const selectedStatus = ref('') // 'submitted', 'not_submitted', 'late', 'on_time'

// Sorting
const sortKey = ref<keyof SubmissionRecord>('due_date')
const sortOrder = ref<'asc' | 'desc'>('desc') // Default to newest first

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Computed properties for interactivity
const filteredAndSortedSubmissionRecords = computed(() => {
  let records = [...allSubmissionRecords.value]

  // Filter by search query
  if (searchQuery.value) {
    const lowerQuery = searchQuery.value.toLowerCase()
    records = records.filter(r =>
      r.student_name?.toLowerCase().includes(lowerQuery) ||
      r.module_title?.toLowerCase().includes(lowerQuery) ||
      r.assessment_name.toLowerCase().includes(lowerQuery)
    )
  }

  // Filter by module
  if (selectedModule.value) {
    records = records.filter(r => r.module_title === selectedModule.value)
  }

  // Filter by status
  if (selectedStatus.value === 'submitted') {
    records = records.filter(r => r.is_submitted)
  } else if (selectedStatus.value === 'not_submitted') {
    records = records.filter(r => !r.is_submitted)
  } else if (selectedStatus.value === 'late') {
    records = records.filter(r => r.is_late)
  } else if (selectedStatus.value === 'on_time') {
    records = records.filter(r => r.is_submitted && !r.is_late)
  }

  // Sort
  records.sort((a, b) => {
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

  return records
})

const totalPages = computed(() => {
  return Math.ceil(filteredAndSortedSubmissionRecords.value.length / itemsPerPage.value)
})

const paginatedSubmissionRecords = computed(() => {
  if (totalPages.value > 0 && currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedSubmissionRecords.value.slice(start, end)
})

// Methods
const fetchSubmissionRecords = async () => {
  try {
    const response = await getSubmissionRecords()
    allSubmissionRecords.value = response.data
  } catch (error: any) {
    console.error('Failed to fetch submission records:', error)
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

const sortBy = (key: keyof SubmissionRecord) => {
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
const currentRecord = ref<Partial<SubmissionRecord>>({
  student_id: 0,
  module_id: 0,
  assessment_name: '',
  due_date: new Date().toISOString().split('T')[0],
  submitted_date: null,
  is_submitted: false,
  is_late: false
})

const openAddModal = () => {
  isEditMode.value = false
  currentRecord.value = {
    student_id: students.value.length ? students.value[0].id : 0,
    module_id: modules.value.length ? modules.value[0].id : 0,
    assessment_name: '',
    due_date: new Date().toISOString().split('T')[0],
    submitted_date: null,
    is_submitted: false,
    is_late: false
  }
  showModal.value = true
}

const openEditModal = (record: SubmissionRecord) => {
  isEditMode.value = true
  currentRecord.value = { ...record, submitted_date: record.submitted_date ? record.submitted_date.split('T')[0] : null }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  message.value = ''
  messageType.value = ''
}

const saveRecord = async () => {
  message.value = ''
  messageType.value = ''
  try {
    if (isEditMode.value && currentRecord.value.id) {
      await updateSubmissionRecord(currentRecord.value.id, currentRecord.value as SubmissionRecord)
      message.value = 'Submission record updated successfully!'
      messageType.value = 'success'
    } else {
      const { id, student_name, module_title, ...newRecord } = currentRecord.value;
      await addSubmissionRecord(newRecord as SubmissionRecord)
      message.value = 'Submission record added successfully!'
      messageType.value = 'success'
    }
    await fetchSubmissionRecords()
    closeModal()
  } catch (error: any) {
    console.error('Failed to save submission record:', error)
    message.value = error.response?.data?.message || 'Failed to save submission record.'
    messageType.value = 'error'
  }
}

const deleteRecord = async (id: number) => {
  if (confirm('Are you sure you want to delete this submission record? (Logical Delete)')) {
    try {
      await deleteSubmissionRecord(id)
      message.value = 'Submission record deleted successfully!'
      messageType.value = 'success'
      await fetchSubmissionRecords()
    } catch (error: any) {
      console.error('Failed to delete submission record:', error)
      message.value = error.response?.data?.message || 'Failed to delete submission record.'
      messageType.value = 'error'
    }
  }
}

onMounted(async () => {
  await fetchStudentsAndModulesForDropdowns()
  await fetchSubmissionRecords()
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
  max-width: 650px; /* Adjusted width for Submission modal */
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

.form-row {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.form-group-checkbox {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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
