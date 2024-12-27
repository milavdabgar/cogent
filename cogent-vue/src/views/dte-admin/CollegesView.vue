<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Manage Colleges</h1>
      <button 
        @click="showAddModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
        Add New College
      </button>
    </div>

    <!-- Search and Filter -->
    <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6">
      <div class="flex gap-4">
        <div class="flex-1">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search colleges..."
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            @input="handleSearch"
          >
        </div>
      </div>
    </div>

    <!-- Colleges Table -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">City</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="college in colleges" :key="college.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ college.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ college.code }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ college.city }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="[
                'px-2 py-1 text-xs rounded-full',
                college.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              ]">
                {{ college.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button 
                @click="editCollege(college)"
                class="text-blue-600 hover:text-blue-800 mr-3">
                Edit
              </button>
              <button 
                @click="confirmDelete(college)"
                class="text-red-600 hover:text-red-800">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit College Modal -->
    <Modal v-model="showAddModal" :title="isEditing ? 'Edit College' : 'Add New College'">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Name</label>
          <input 
            v-model="collegeForm.name"
            type="text"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Code</label>
          <input 
            v-model="collegeForm.code"
            type="text"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">City</label>
          <input 
            v-model="collegeForm.city"
            type="text"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Status</label>
          <select 
            v-model="collegeForm.is_active"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            <option :value="true">Active</option>
            <option :value="false">Inactive</option>
          </select>
        </div>
        <div class="flex justify-end gap-3">
          <button 
            type="button"
            @click="showAddModal = false"
            class="px-4 py-2 border rounded-md hover:bg-gray-50">
            Cancel
          </button>
          <button 
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            {{ isEditing ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal v-model="showDeleteModal" title="Confirm Delete">
      <div class="p-4">
        <p>Are you sure you want to delete this college?</p>
        <div class="mt-4 flex justify-end gap-3">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 border rounded-md hover:bg-gray-50">
            Cancel
          </button>
          <button 
            @click="deleteCollege"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
            Delete
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDTEAdminStore } from '@/stores/dte-admin'
import Modal from '@/components/Modal.vue'

const dteAdminStore = useDTEAdminStore()
const colleges = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const selectedCollege = ref(null)
const collegeForm = ref({
  name: '',
  code: '',
  city: '',
  is_active: true
})

onMounted(async () => {
  await fetchColleges()
})

const fetchColleges = async () => {
  await dteAdminStore.fetchColleges()
  colleges.value = dteAdminStore.colleges
}

const handleSearch = async () => {
  await dteAdminStore.fetchColleges({ search: searchQuery.value })
  colleges.value = dteAdminStore.colleges
}

const resetForm = () => {
  collegeForm.value = {
    name: '',
    code: '',
    city: '',
    is_active: true
  }
  isEditing.value = false
  selectedCollege.value = null
}

const editCollege = (college) => {
  isEditing.value = true
  selectedCollege.value = college
  collegeForm.value = { ...college }
  showAddModal.value = true
}

const confirmDelete = (college) => {
  selectedCollege.value = college
  showDeleteModal.value = true
}

const deleteCollege = async () => {
  try {
    await dteAdminStore.deleteCollege(selectedCollege.value.id)
    showDeleteModal.value = false
    await fetchColleges()
  } catch (error) {
    console.error('Failed to delete college:', error)
  }
}

const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      await dteAdminStore.updateCollege(selectedCollege.value.id, collegeForm.value)
    } else {
      await dteAdminStore.createCollege(collegeForm.value)
    }
    showAddModal.value = false
    resetForm()
    await fetchColleges()
  } catch (error) {
    console.error('Failed to save college:', error)
  }
}
</script>
