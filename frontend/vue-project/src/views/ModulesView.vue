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

    <!-- Modal logic remains similar, but needs to be adapted -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getModules, type Module } from '@/api/moduleService'
// Assume add/update/delete services exist in moduleService
// import { addModule, updateModule, deleteModule } from '@/api/moduleService'

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

// Modal logic (placeholder, needs full implementation)
const showModal = ref(false)
const isEditMode = ref(false)
const currentModule = ref<Partial<Module>>({})
const openAddModal = () => { /* ... */ }
const openEditModal = (module: Module) => { /* ... */ }
const handleDeleteModule = async (id: number) => { /* ... */ }
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
</style>
