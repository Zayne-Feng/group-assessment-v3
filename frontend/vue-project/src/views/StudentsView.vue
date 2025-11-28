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
    <!-- Student Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3>{{ isEditMode ? 'Edit Student' : 'Add New Student' }}</h3>
        <form @submit.prevent="handleSaveStudent">
          <div class="form-group">
            <label for="student_number">Student Number:</label>
            <input type="text" id="student_number" v-model="currentStudent.student_number" required />
          </div>
          <div class="form-group">
            <label for="full_name">Full Name:</label>
            <input type="text" id="full_name" v-model="currentStudent.full_name" required />
          </div>
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="currentStudent.email" required />
          </div>
          <div class="form-group">
            <label for="course_name">Course:</label>
            <input type="text" id="course_name" v-model="currentStudent.course_name" />
          </div>
          <div class="form-group">
            <label for="year_of_study">Year of Study:</label>
            <input type="number" id="year_of_study" v-model="currentStudent.year_of_study" />
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

// Modal logic
const showModal = ref(false)
const isEditMode = ref(false)
const currentStudent = ref<Student>({ student_number: '', full_name: '', email: '', course_name: '', year_of_study: undefined })

const openAddModal = () => {
  console.log('openAddModal called'); // Added for debugging
  isEditMode.value = false;
  currentStudent.value = { student_number: '', full_name: '', email: '', course_name: '', year_of_study: undefined }; // Reset for new student
  showModal.value = true;
};

const openEditModal = (student: Student) => {
  isEditMode.value = true;
  currentStudent.value = { ...student }; // Copy student data for editing
  showModal.value = true;
};

const handleSaveStudent = async () => {
  try {
    if (isEditMode.value) {
      if (currentStudent.value.id) {
        await updateStudent(currentStudent.value.id, currentStudent.value);
        showMessage('Student updated successfully!', 'success');
      } else {
        showMessage('Error: Student ID is missing for update.', 'error');
      }
    } else {
      await addStudent(currentStudent.value);
      showMessage('Student added successfully!', 'success');
    }
    showModal.value = false;
    await fetchStudents(); // Refresh the list
  } catch (error: any) {
    console.error('Failed to save student:', error);
    showMessage('Failed to save student.', 'error');
  }
};

const handleDeleteStudent = async (id: number) => {
  if (confirm('Are you sure you want to delete this student?')) {
    try {
      await deleteStudent(id);
      showMessage('Student deleted successfully!', 'success');
      await fetchStudents(); // Refresh the list
    } catch (error: any) {
      console.error('Failed to delete student:', error);
      showMessage('Failed to delete student.', 'error');
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
.form-group input[type="number"] {
  width: calc(100% - 20px); /* Adjust for padding */
  padding: 0.75rem 10px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
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
