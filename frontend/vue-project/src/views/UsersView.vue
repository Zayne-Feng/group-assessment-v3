<template>
  <div>
    <div class="page-header">
      <div class="filter-bar">
        <input type="text" v-model="searchQuery" placeholder="Search by username or role..." class="search-input">
        <select v-model="selectedRole" class="filter-select">
          <option value="">All Roles</option>
          <option v-for="role in uniqueRoles" :key="role" :value="role">{{ role }}</option>
        </select>
        <select v-model="selectedStatus" class="filter-select">
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
      <button @click="openAddModal" v-if="authStore.isAdmin" class="btn-primary">Add New User</button>
    </div>

    <div class="table-container card">
      <div v-if="paginatedUsers.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('username')" class="sortable">
                Username <span v-if="sortKey === 'username'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('role')" class="sortable">
                Role <span v-if="sortKey === 'role'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('created_at')" class="sortable">
                Created At <span v-if="sortKey === 'created_at'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('is_active')" class="sortable">
                Status <span v-if="sortKey === 'is_active'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="actions-header" v-if="authStore.isAdmin">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.role }}</td>
              <td>{{ new Date(user.created_at).toLocaleDateString() }}</td>
              <td>
                <span :class="['status-badge', user.is_active ? 'status-success' : 'status-danger']">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="action-buttons" v-if="authStore.isAdmin">
                <button @click="openEditModal(user)" class="btn-secondary btn-sm">Edit</button>
                <button @click="openResetPasswordModal(user)" class="btn-warning btn-sm">Reset Password</button>
                <button @click="handleDeleteUser(user.id!)" class="btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No users match your criteria.</p>
    </div>

    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
    </div>

    <!-- Add/Edit User Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>{{ isEditMode ? 'Edit User' : 'Add User' }}</h2>
        <form @submit.prevent="saveUser" class="modal-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input id="username" type="text" v-model="currentUser.username" required>
          </div>
          <div class="form-group" v-if="!isEditMode">
            <label for="password">Password</label>
            <input id="password" type="password" v-model="currentUser.password" required>
          </div>
          <div class="form-group">
            <label for="role">Role</label>
            <select id="role" v-model="currentUser.role" required>
              <option value="admin">Admin</option>
              <option value="course_director">Course Director</option>
              <option value="wellbeing_officer">Wellbeing Officer</option>
              <option value="student">Student</option>
            </select>
          </div>
          <div class="form-group-checkbox">
            <input id="isActive" type="checkbox" v-model="currentUser.is_active">
            <label for="isActive">Active</label>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn-primary">Save</button>
            <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
          </div>
        </form>
        <div v-if="message" :class="['message', messageType]">{{ message }}</div>
      </div>
    </div>

    <!-- Reset Password Modal -->
    <div v-if="showResetPasswordModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Reset Password for {{ currentUser.username }}</h2>
        <form @submit.prevent="handleResetPassword" class="modal-form">
          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input id="newPassword" type="password" v-model="newPassword" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn-primary">Save New Password</button>
            <button type="button" @click="closeResetPasswordModal" class="btn-secondary">Cancel</button>
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
import { getUsers, addUser, updateUser, deleteUser, resetUserPassword, type User } from '@/api/userService'

const authStore = useAuthStore()

// Data
const allUsers = ref<User[]>([])
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

// Filtering and Searching
const searchQuery = ref('')
const selectedRole = ref('')
const selectedStatus = ref('')

// Sorting
const sortKey = ref<keyof User>('username')
const sortOrder = ref<'asc' | 'desc'>('asc')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Computed properties
const uniqueRoles = computed(() => {
  const roles = allUsers.value.map(u => u.role).filter(Boolean) as string[]
  return [...new Set(roles)]
})

const filteredAndSortedUsers = computed(() => {
  let users = [...allUsers.value]
  if (searchQuery.value) {
    const lowerQuery = searchQuery.value.toLowerCase()
    users = users.filter(u => u.username.toLowerCase().includes(lowerQuery) || u.role.toLowerCase().includes(lowerQuery))
  }
  if (selectedRole.value) {
    users = users.filter(u => u.role === selectedRole.value)
  }
  if (selectedStatus.value === 'active') {
    users = users.filter(u => u.is_active)
  } else if (selectedStatus.value === 'inactive') {
    users = users.filter(u => !u.is_active)
  }
  users.sort((a, b) => {
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
  return users
})

const totalPages = computed(() => Math.ceil(filteredAndSortedUsers.value.length / itemsPerPage.value))

const paginatedUsers = computed(() => {
  if (totalPages.value > 0 && currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedUsers.value.slice(start, end)
})

// Methods
const fetchUsers = async () => {
  try {
    const response = await getUsers()
    allUsers.value = response.data
  } catch (error: any) {
    console.error('Failed to fetch users:', error)
  }
}

const sortBy = (key: keyof User) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }

// Modal logic for Add/Edit User
const showModal = ref(false)
const isEditMode = ref(false)
const currentUser = ref<Partial<User>>({ username: '', password: '', role: 'student', is_active: true })

const openAddModal = () => {
  isEditMode.value = false
  currentUser.value = { username: '', password: '', role: 'student', is_active: true }
  showModal.value = true
}

const openEditModal = (user: User) => {
  isEditMode.value = true
  currentUser.value = { ...user }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  message.value = ''
}

const saveUser = async () => {
  message.value = ''
  try {
    if (isEditMode.value && currentUser.value.id) {
      await updateUser(currentUser.value.id, currentUser.value)
      message.value = 'User updated successfully!'
    } else {
      if (!currentUser.value.password) {
        message.value = 'Password is required for new users.'
        messageType.value = 'error'
        return
      }
      await addUser(currentUser.value as User)
      message.value = 'User added successfully!'
    }
    messageType.value = 'success'
    await fetchUsers()
    closeModal()
  } catch (error: any) {
    console.error('Failed to save user:', error)
    message.value = error.response?.data?.message || 'Failed to save user.'
    messageType.value = 'error'
  }
}

// Modal logic for Reset Password
const showResetPasswordModal = ref(false)
const newPassword = ref('')

const openResetPasswordModal = (user: User) => {
  currentUser.value = { ...user } // Store the user whose password is being reset
  newPassword.value = ''
  showResetPasswordModal.value = true
}

const closeResetPasswordModal = () => {
  showResetPasswordModal.value = false
  message.value = ''
}

const handleResetPassword = async () => {
  if (!currentUser.value.id || !newPassword.value) {
    message.value = 'User ID is missing or new password is empty.'
    messageType.value = 'error'
    return
  }
  message.value = ''
  try {
    await resetUserPassword(currentUser.value.id, newPassword.value)
    message.value = 'Password reset successfully!'
    messageType.value = 'success'
    closeResetPasswordModal()
  } catch (error: any) {
    console.error('Failed to reset password:', error)
    message.value = error.response?.data?.message || 'Failed to reset password.'
    messageType.value = 'error'
  }
}

const handleDeleteUser = async (id: number) => {
  if (confirm('Are you sure you want to delete this user? (Logical Delete)')) {
    try {
      await deleteUser(id)
      message.value = 'User deleted successfully!'
      messageType.value = 'success'
      await fetchUsers()
    } catch (error: any) {
      console.error('Failed to delete user:', error)
      message.value = error.response?.data?.message || 'Failed to delete user.'
      messageType.value = 'error'
    }
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
/* Styles remain the same, but adding a warning button style */
.btn-warning {
  background-color: #f59e0b; /* Amber */
  color: white;
  border: none;
}
.btn-warning:hover {
  background-color: #d97706;
}

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

/* Modal Specific Styles */
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
  max-width: 500px;
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
.modal-form .form-group input[type="password"],
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
