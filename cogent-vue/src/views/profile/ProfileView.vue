<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-tabs v-model="activeTab">
            <v-tab value="profile">Profile</v-tab>
            <v-tab value="security">Security</v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="activeTab">
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <v-form @submit.prevent="handleProfileUpdate" v-model="profileForm.valid">
                  <v-row>
                    <!-- Edit Mode Toggle -->
                    <v-col cols="12" class="text-right">
                      <v-btn
                        :color="isEditing ? 'error' : 'primary'"
                        @click="toggleEditMode"
                        :prepend-icon="isEditing ? 'mdi-close' : 'mdi-pencil'"
                      >
                        {{ isEditing ? 'Cancel' : 'Edit' }}
                      </v-btn>
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileForm.first_name"
                        label="First Name"
                        :readonly="!isEditing"
                        :rules="[v => !!v || 'First name is required']"
                        variant="outlined"
                        :class="{ 'editable': isEditing }"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileForm.last_name"
                        label="Last Name"
                        :readonly="!isEditing"
                        :rules="[v => !!v || 'Last name is required']"
                        variant="outlined"
                        :class="{ 'editable': isEditing }"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileForm.email"
                        label="Email"
                        type="email"
                        readonly
                        variant="outlined"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileForm.phone_number"
                        label="Phone Number"
                        :readonly="!isEditing"
                        variant="outlined"
                        :class="{ 'editable': isEditing }"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-menu
                        v-if="isEditing"
                        v-model="dateMenu"
                        :close-on-content-click="false"
                      >
                        <template v-slot:activator="{ props }">
                          <v-text-field
                            v-model="formattedDateOfBirth"
                            label="Date of Birth"
                            readonly
                            v-bind="props"
                            variant="outlined"
                            :class="{ 'editable': isEditing }"
                            prepend-icon="mdi-calendar"
                          />
                        </template>
                        <v-date-picker
                          v-model="profileForm.date_of_birth"
                          @update:model-value="dateMenu = false"
                        />
                      </v-menu>
                      <v-text-field
                        v-else
                        v-model="formattedDateOfBirth"
                        label="Date of Birth"
                        readonly
                        variant="outlined"
                      />
                    </v-col>

                    <!-- Role-specific fields -->
                    <template v-if="profileStore.profile?.role === 'student'">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.enrollment_number"
                          label="Enrollment Number"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.current_semester"
                          label="Current Semester"
                          type="number"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[
                            v => (!v || (v >= 1 && v <= 8)) || 'Semester must be between 1 and 8'
                          ]"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.department"
                          label="Department"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                        />
                      </v-col>
                    </template>

                    <template v-else-if="['faculty', 'hod', 'lab_assistant'].includes(profileStore.profile?.role)">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.department"
                          label="Department"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.qualification"
                          label="Qualification"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                        />
                      </v-col>
                      <v-col cols="12" md="6" v-if="profileStore.profile?.role === 'faculty'">
                        <v-text-field
                          v-model="profileForm.specialization"
                          label="Specialization"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                        />
                      </v-col>
                    </template>
                  </v-row>

                  <v-card-actions v-if="isEditing">
                    <v-spacer />
                    <v-btn
                      color="primary"
                      type="submit"
                      :loading="profileStore.loading"
                      :disabled="!profileForm.valid"
                    >
                      Save Changes
                    </v-btn>
                  </v-card-actions>
                </v-form>
              </v-window-item>

              <!-- Security Tab -->
              <v-window-item value="security">
                <v-form @submit.prevent="handlePasswordChange" v-model="passwordForm.valid">
                  <v-text-field
                    v-model="passwordForm.current_password"
                    label="Current Password"
                    type="password"
                    :rules="[v => !!v || 'Current password is required']"
                    variant="outlined"
                  />
                  <v-text-field
                    v-model="passwordForm.new_password"
                    label="New Password"
                    type="password"
                    :rules="[
                      v => !!v || 'New password is required',
                      v => v.length >= 8 || 'Password must be at least 8 characters'
                    ]"
                    variant="outlined"
                  />
                  <v-text-field
                    v-model="passwordForm.confirm_password"
                    label="Confirm New Password"
                    type="password"
                    :rules="[
                      v => !!v || 'Please confirm your password',
                      v => v === passwordForm.new_password || 'Passwords must match'
                    ]"
                    variant="outlined"
                  />

                  <v-card-actions>
                    <v-spacer />
                    <v-btn
                      color="primary"
                      type="submit"
                      :loading="profileStore.loading"
                      :disabled="!passwordForm.valid"
                    >
                      Change Password
                    </v-btn>
                  </v-card-actions>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success/Error Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useAuthStore } from '@/stores/auth'

const profileStore = useProfileStore()
const authStore = useAuthStore()

const activeTab = ref('profile')
const snackbar = ref({ show: false, text: '', color: 'success' })
const isEditing = ref(false)
const dateMenu = ref(false)

const profileForm = ref({
  valid: true,
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  date_of_birth: null,
  enrollment_number: '',
  current_semester: null,
  department: '',
  qualification: '',
  specialization: ''
})

const passwordForm = ref({
  valid: true,
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// Format date for display
const formattedDateOfBirth = computed(() => {
  if (!profileForm.value.date_of_birth) return ''
  const date = new Date(profileForm.value.date_of_birth)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

onMounted(async () => {
  try {
    await profileStore.fetchProfile()
    if (profileStore.profile) {
      // Map basic fields
      const basicFields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']
      basicFields.forEach(field => {
        if (profileStore.profile[field]) {
          profileForm.value[field] = profileStore.profile[field]
        }
      })

      // Map role-specific details
      if (profileStore.profile.role === 'student' && profileStore.profile.student_details) {
        const { enrollment_number, current_semester, department } = profileStore.profile.student_details
        profileForm.value.enrollment_number = enrollment_number
        profileForm.value.current_semester = current_semester
        profileForm.value.department = department
      } else if (profileStore.profile.role === 'faculty' && profileStore.profile.faculty_details) {
        const { department, qualification, specialization } = profileStore.profile.faculty_details
        profileForm.value.department = department
        profileForm.value.qualification = qualification
        profileForm.value.specialization = specialization
      }
    }
  } catch (error) {
    showError('Failed to load profile')
  }
})

const toggleEditMode = () => {
  if (isEditing.value) {
    // Reset form to original values
    if (profileStore.profile) {
      Object.keys(profileForm.value).forEach(key => {
        if (key !== 'valid' && profileStore.profile[key]) {
          profileForm.value[key] = profileStore.profile[key]
        }
      })
    }
  }
  isEditing.value = !isEditing.value
}

async function handleProfileUpdate() {
  try {
    await profileStore.updateProfile(profileForm.value)
    showSuccess('Profile updated successfully')
    isEditing.value = false
  } catch (error) {
    showError('Failed to update profile')
  }
}

async function handlePasswordChange() {
  try {
    await profileStore.changePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password
    })
    showSuccess('Password changed successfully')
    // Reset password form
    passwordForm.value = {
      valid: true,
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    showError('Failed to change password')
  }
}

function showSuccess(text) {
  snackbar.value = {
    show: true,
    text,
    color: 'success'
  }
}

function showError(text) {
  snackbar.value = {
    show: true,
    text,
    color: 'error'
  }
}
</script>

<style scoped>
.editable {
  background-color: #f5f5f5;
}

.v-text-field.editable :deep(.v-field__outline) {
  border-color: var(--v-primary-base) !important;
}
</style>