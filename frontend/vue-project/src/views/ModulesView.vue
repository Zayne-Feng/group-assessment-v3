<template>
  <div>
    <div class="page-header">
      <div class="filter-bar">
        <input type="text" v-model="searchQuery" placeholder="Search by title or code..." class="search-input">
      </div>
      <button @click="openAddModal" v-if="authStore.isAdmin" class="btn-primary">Add New Module</button>
    </div>

    <div class="table-container card">
      <div v-if="paginatedModules.length" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('module_code')" class="sortable">
                Code <span v-if="sortKey === 'module_code'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('module_title')" class="sortable">
                Title <span v-if="sortKey === 'module_title'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('credit')" class="sortable">
                Credit <span v-if="sortKey === 'credit'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortBy('academic_year')" class="sortable">
                Academic Year <span v-if="sortKey === 'academic_year'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="actions-header" v-if="authStore.isAdmin">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="module in paginatedModules" :key="module.id">
              <td>{{ module.module_code }}</td>
              <td>{{ module.module_title }}</td>
              <td>{{ module.credit }}</td>
              <td>{{ module.academic_year }}</td>
              <td class="action-buttons" v-if="authStore.isAdmin">
                <button @click="openEditModal(module)" class="btn-secondary btn-sm">Edit</button>
                <button @click="handleDeleteModule(module.id!)" class="btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-data-message">No modules match your criteria.</p>
    </div>

    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages" class="btn-secondary">Next</button>
    </div>

    <!-- Module Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3>{{ isEditMode ? 'Edit Module' : 'Add New Module' }}</h3>
        <form @submit.prevent="handleSaveModule">
          <div class="form-group">
            <label for="module_code">Module Code:</label>
            <input type="text" id="module_code" v-model="currentModule.module_code" required />
          </div>
          <div class="form-group">
            <label for="module_title">Module Title:</label>
            <input type="text" id="module_title" v-model="currentModule.module_title" required />
          </div>
          <div class="form-group">
            <label for="credit">Credit:</label>
            <input type="number" id="credit" v-model="currentModule.credit" required />
          </div>
          <div class="form-group">
            <label for="academic_year">Academic Year:</label>
            <input type="text" id="academic_year" v-model="currentModule.academic_year" />
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
import { useAuthStore } from '@/stores/auth'
import { getModules, addModule, updateModule, deleteModule, type Module } from '@/api/moduleService'

const authStore = useAuthStore()

// Data
const allModules = ref<Module[]>([])
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

// Filtering and Searching
const searchQuery = ref('')

// Sorting
const sortKey = ref<keyof Module>('module_title')
const sortOrder = ref<'asc' | 'desc'>('asc')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Computed properties
const filteredAndSortedModules = computed(() => {
  let modules = [...allModules.value]

  if (searchQuery.value) {
    const lowerQuery = searchQuery.value.toLowerCase()
    modules = modules.filter(m =>
      m.module_title.toLowerCase().includes(lowerQuery) ||
      m.module_code.toLowerCase().includes(lowerQuery)
    )
  }

  modules.sort((a, b) => {
    const valA = a[sortKey.value]
    const valB = b[sortKey.value]
    if (valA === undefined || valB === undefined) return 0

    let comparison = 0;
    if (valA > valB) comparison = 1;
    else if (valA < valB) comparison = -1;
    return sortOrder.value === 'asc' ? comparison : -comparison;
  })

  return modules
})

const totalPages = computed(() => {
  return Math.ceil(filteredAndSortedModules.value.length / itemsPerPage.value)
})

const paginatedModules = computed(() => {
  if (totalPages.value > 0 && currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedModules.value.slice(start, end)
})

// Methods
const fetchModules = async () => {
  try {
    const response = await getModules()
    allModules.value = response.data
  } catch (error: any) {
    console.error('Failed to fetch modules:', error)
  }
}

const sortBy = (key: keyof Module) => {
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

onMounted(fetchModules)

// Modal logic
const showModal = ref(false)
const isEditMode = ref(false)
const currentModule = ref<Module>({ module_code: '', module_title: '', credit: 0, academic_year: '' })

const openAddModal = () => {
  console.log('openAddModal called'); // Added for debugging
  isEditMode.value = false;
  currentModule.value = { module_code: '', module_title: '', credit: 0, academic_year: '' }; // Reset for new module
  showModal.value = true;
};

const openEditModal = (module: Module) => {
  isEditMode.value = true;
  currentModule.value = { ...module }; // Copy module data for editing
  showModal.value = true;
};

const handleSaveModule = async () => {
  try {
    if (isEditMode.value) {
      if (currentModule.value.id) {
        await updateModule(currentModule.value.id, currentModule.value);
        showMessage('Module updated successfully!', 'success');
      } else {
        showMessage('Error: Module ID is missing for update.', 'error');
      }
    } else {
      await addModule(currentModule.value);
      showMessage('Module added successfully!', 'success');
    }
    showModal.value = false;
    await fetchModules(); // Refresh the list
  } catch (error: any) {
    console.error('Failed to save module:', error);
    showMessage('Failed to save module.', 'error');
  }
};

const handleDeleteModule = async (id: number) => {
  if (confirm('Are you sure you want to delete this module?')) {
    try {
      await deleteModule(id);
      showMessage('Module deleted successfully!', 'success');
      await fetchModules(); // Refresh the list
    } catch (error: any) {
      console.error('Failed to delete module:', error);
      showMessage('Failed to delete module.', 'error');
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
/* Using the same refined styles as StudentsView.vue */
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
