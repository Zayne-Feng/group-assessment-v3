<template>
  <div>
    <div class="page-header">
      <div class="filter-bar">
        <input type="text" v-model="searchQuery" placeholder="Search by name or student number..." class="search-input">
        <select v-model="selectedCourse" class="filter-select">
          <option value="">All Courses</option>
          <option v-for="course in uniqueCourses" :key="course" :value="course">{{ course }}</option>
        </select>
      </div>
      <button @click="openAddModal" class="btn-primary">Add New Student</button>
    </div>

    <div class="table-container card">
      <div v-if="paginatedStudents.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('student_number')" class="sortable">
                Student Number <span v-if="sortKey === 'student_number'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('full_name')" class="sortable">
                Full Name <span v-if="sortKey === 'full_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th>Email</th>
              <th @click="sortBy('course_name')" class="sortable">
                Course <span v-if="sortKey === 'course_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('year_of_study')" class="sortable">
                Year <span v-if="sortKey === 'year_of_study'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="actions-header">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in paginatedStudents" :key="student.id">
              <td>{{ student.student_number }}</td>
              <td>
                <router-link :to="{ name: 'student-detail', params: { id: student.id } }" class="student-link">
                  {{ student.full_name }}
                </router-link>
              </td>
              <td>{{ student.email }}</td>
              <td>{{ student.course_name }}</td>
              <td>{{ student.year_of_study }}</td>
              <td class="action-buttons">
                <button @click="openEditModal(student)" class="btn-secondary btn-sm">Edit</button>
                <button @click="handleDeleteStudent(student.id!)" class="btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No students match your criteria.</p>
    </div>

    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
    </div>

    <!-- Modal logic remains unchanged -->
  </div>
</template>

<script setup lang="ts">
// Script content remains the same
import { ref, onMounted, computed } from 'vue'
import { getStudents, addStudent, updateStudent, deleteStudent, type Student } from '@/api/studentService'

const allStudents = ref<Student[]>([])
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')
const searchQuery = ref('')
const selectedCourse = ref('')
const sortKey = ref<keyof Student>('full_name')
const sortOrder = ref<'asc' | 'desc'>('asc')
const currentPage = ref(1)
const itemsPerPage = ref(10)

const uniqueCourses = computed(() => {
  const courses = allStudents.value.map(s => s.course_name).filter(Boolean) as string[]
  return [...new Set(courses)]
})

const filteredAndSortedStudents = computed(() => {
  let students = [...allStudents.value]
  if (searchQuery.value) {
    const lowerQuery = searchQuery.value.toLowerCase()
    students = students.filter(s =>
      s.full_name.toLowerCase().includes(lowerQuery) ||
      s.student_number.toLowerCase().includes(lowerQuery)
    )
  }
  if (selectedCourse.value) {
    students = students.filter(s => s.course_name === selectedCourse.value)
  }
  students.sort((a, b) => {
    const valA = a[sortKey.value]
    const valB = b[sortKey.value]
    if (valA === undefined || valB === undefined) return 0
    let comparison = 0;
    if (valA > valB) comparison = 1;
    else if (valA < valB) comparison = -1;
    return sortOrder.value === 'asc' ? comparison : -comparison;
  })
  return students
})

const totalPages = computed(() => {
  return Math.ceil(filteredAndSortedStudents.value.length / itemsPerPage.value)
})

const paginatedStudents = computed(() => {
  if (totalPages.value > 0 && currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedStudents.value.slice(start, end)
})

const fetchStudents = async () => {
  try {
    const response = await getStudents()
    allStudents.value = response.data
  } catch (error: any) {
    console.error('Failed to fetch students:', error)
  }
}

const sortBy = (key: keyof Student) => {
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

onMounted(fetchStudents)

// Modal logic (omitted for brevity)
const showModal = ref(false)
const isEditMode = ref(false)
const currentStudent = ref<Student>({ student_number: '', full_name: '', email: '' })
const openAddModal = () => { /* ... */ }
const openEditModal = (student: Student) => { /* ... */ }
const handleDeleteStudent = async (id: number) => { /* ... */ }
</script>

<style scoped>
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

.student-link {
  color: #3498db; /* A distinct, classic link blue */
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.student-link:hover {
  text-decoration: underline;
  color: var(--vt-c-indigo); /* On hover, use the main theme color */
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
</style>
