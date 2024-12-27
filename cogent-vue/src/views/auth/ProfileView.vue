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
                <v-form @submit.prevent="handleSubmit" v-model="profileForm.valid">
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
                        variant="outlined"
                        :class="{ 'editable': isEditing }"
                        :rules="[v => !!v || 'First name is required']"
                        :loading="authStore.loading"
                        :error-messages="authStore.error"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileForm.last_name"
                        label="Last Name"
                        :readonly="!isEditing"
                        variant="outlined"
                        :class="{ 'editable': isEditing }"
                        :rules="[v => !!v || 'Last name is required']"
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
                      <v-text-field
                        v-model="profileForm.date_of_birth"
                        type="date"
                        label="Date of Birth"
                        :readonly="!isEditing"
                        variant="outlined"
                        :class="{ 'editable': isEditing }"
                        prepend-icon="mdi-calendar"
                      />
                    </v-col>

                    <!-- Role-specific fields -->
                    <template v-if="authStore.profile?.role === 'student'">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.student_details.enrollment_number"
                          label="Enrollment Number"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Enrollment number is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.student_details.department"
                          label="Department"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Department is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.student_details.current_semester"
                          label="Current Semester"
                          type="number"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[
                            v => !!v || 'Current semester is required',
                            v => (!v || (v >= 1 && v <= 8)) || 'Semester must be between 1 and 8'
                          ]"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.student_details.date_of_admission"
                          type="date"
                          label="Date of Admission"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          prepend-icon="mdi-calendar"
                        />
                      </v-col>
                    </template>

                    <template v-if="authStore.profile?.role === 'faculty'">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.faculty_details.department"
                          label="Department"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Department is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.faculty_details.qualification"
                          label="Qualification"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Qualification is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.faculty_details.specialization"
                          label="Specialization"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Specialization is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.faculty_details.date_of_joining"
                          type="date"
                          label="Date of Joining"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          prepend-icon="mdi-calendar"
                        />
                      </v-col>
                    </template>

                    <template v-if="authStore.profile?.role === 'hod'">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.hod_details.department"
                          label="Department"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Department is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.hod_details.qualification"
                          label="Qualification"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Qualification is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.hod_details.experience_years"
                          label="Years of Experience"
                          type="number"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Years of experience is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.hod_details.date_of_joining"
                          type="date"
                          label="Date of Joining"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          prepend-icon="mdi-calendar"
                        />
                      </v-col>
                    </template>

                    <template v-if="authStore.profile?.role === 'principal'">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.principal_details.qualification"
                          label="Qualification"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Qualification is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.principal_details.experience_years"
                          label="Years of Experience"
                          type="number"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Years of experience is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.principal_details.date_of_joining"
                          type="date"
                          label="Date of Joining"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          prepend-icon="mdi-calendar"
                          :rules="[v => !!v || 'Date of joining is required']"
                        />
                      </v-col>
                    </template>

                    <template v-if="authStore.profile?.role === 'lab_assistant'">
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.lab_assistant_details.department"
                          label="Department"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Department is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.lab_assistant_details.lab_type"
                          label="Lab Type"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          :rules="[v => !!v || 'Lab type is required']"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileForm.lab_assistant_details.date_of_joining"
                          type="date"
                          label="Date of Joining"
                          :readonly="!isEditing"
                          variant="outlined"
                          :class="{ 'editable': isEditing }"
                          prepend-icon="mdi-calendar"
                        />
                      </v-col>
                    </template>

                    <v-card-actions v-if="isEditing">
                      <v-spacer />
                      <v-btn
                        color="primary"
                        type="submit"
                        :loading="authStore.loading"
                        :disabled="!profileForm.valid"
                      >
                        Save Changes
                      </v-btn>
                    </v-card-actions>
                  </v-row>
                </v-form>
              </v-window-item>

              <!-- Security Tab -->
              <v-window-item value="security">
                <v-form 
                  ref="passwordFormRef"
                  @submit.prevent="handlePasswordChange" 
                  v-model="passwordForm.valid"
                >
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
                      :loading="authStore.loading"
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
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

const authStore = useAuthStore()

const passwordFormRef = ref(null)

const activeTab = ref('profile')
const snackbar = ref({ show: false, text: '', color: 'success' })
const isEditing = ref(false)

const profileForm = ref({
  valid: true,
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  date_of_birth: '',
  student_details: {
    enrollment_number: '',
    department: '',
    date_of_admission: '',
    current_semester: null
  },
  faculty_details: {
    department: '',
    date_of_joining: '',
    qualification: '',
    specialization: ''
  },
  hod_details: {
    department: '',
    date_of_joining: '',
    qualification: '',
    experience_years: null
  },
  principal_details: {
    date_of_joining: '',
    qualification: '',
    experience_years: null
  },
  lab_assistant_details: {
    department: '',
    date_of_joining: '',
    lab_type: ''
  }
})

const passwordForm = ref({
  valid: true,
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// Format date for display and input
const formatDate = (date) => {
  if (!date) return ''
  try {
    const d = new Date(date)
    if (isNaN(d.getTime())) return ''
    return d.toISOString().split('T')[0] // Returns YYYY-MM-DD format
  } catch (e) {
    console.error('Error formatting date:', e)
    return ''
  }
}

onMounted(async () => {
  try {
    await authStore.fetchProfile()
    initializeForm()
  } catch (error) {
    console.error('Error fetching profile:', error)
    showError('Failed to load profile')
  }
})

const handleSubmit = async () => {
  try {
    await authStore.updateProfile(profileForm.value)
    isEditing.value = false
    snackbar.value = {
      show: true,
      text: 'Profile updated successfully',
      color: 'success'
    }
  } catch (error) {
    snackbar.value = {
      show: true,
      text: error.message || 'Failed to update profile',
      color: 'error'
    }
  }
}

const toggleEditMode = () => {
  if (isEditing.value) {
    // Reset form when canceling edit
    if (authStore.profile) {
      // Reset basic fields
      const { first_name, last_name, email, phone_number, date_of_birth } = authStore.profile
      
      profileForm.value.first_name = first_name
      profileForm.value.last_name = last_name
      profileForm.value.email = email
      profileForm.value.phone_number = phone_number
      profileForm.value.date_of_birth = formatDate(date_of_birth)

      // Reset role-specific fields
      if (authStore.profile.role === 'student' && authStore.profile.student_details) {
        const { enrollment_number, department, date_of_admission, current_semester } = authStore.profile.student_details
        profileForm.value.student_details.enrollment_number = enrollment_number
        profileForm.value.student_details.department = department
        profileForm.value.student_details.date_of_admission = formatDate(date_of_admission)
        profileForm.value.student_details.current_semester = current_semester
      } else if (authStore.profile.role === 'faculty' && authStore.profile.faculty_details) {
        const { department, date_of_joining, qualification, specialization } = authStore.profile.faculty_details
        profileForm.value.faculty_details.department = department
        profileForm.value.faculty_details.date_of_joining = formatDate(date_of_joining)
        profileForm.value.faculty_details.qualification = qualification
        profileForm.value.faculty_details.specialization = specialization
      } else if (authStore.profile.role === 'hod' && authStore.profile.hod_details) {
        const { department, date_of_joining, qualification, experience_years } = authStore.profile.hod_details
        profileForm.value.hod_details.department = department
        profileForm.value.hod_details.date_of_joining = formatDate(date_of_joining)
        profileForm.value.hod_details.qualification = qualification
        profileForm.value.hod_details.experience_years = experience_years
      } else if (authStore.profile.role === 'principal') {
        // Initialize principal_details if null
        if (!authStore.profile.principal_details) {
          authStore.profile.principal_details = {
            qualification: '',
            experience_years: null,
            date_of_joining: null
          }
        }
        const { date_of_joining, qualification, experience_years } = authStore.profile.principal_details || {}
        profileForm.value.principal_details.date_of_joining = formatDate(date_of_joining)
        profileForm.value.principal_details.qualification = qualification || ''
        profileForm.value.principal_details.experience_years = experience_years || null
      } else if (authStore.profile.role === 'lab_assistant' && authStore.profile.lab_assistant_details) {
        const { department, date_of_joining, lab_type } = authStore.profile.lab_assistant_details
        profileForm.value.lab_assistant_details.department = department
        profileForm.value.lab_assistant_details.date_of_joining = formatDate(date_of_joining)
        profileForm.value.lab_assistant_details.lab_type = lab_type
      }
    }
  }
  isEditing.value = !isEditing.value
}

async function handlePasswordChange() {
  try {
    await authStore.changePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password,
      confirm_password: passwordForm.value.confirm_password
    })
    showSuccess('Password changed successfully')
    // Reset form and validation
    passwordForm.value = {
      valid: true,
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
    // Reset form validation
    if (passwordFormRef.value) {
      passwordFormRef.value.reset()
    }
    // Wait for success message then logout and redirect
    await new Promise(resolve => setTimeout(resolve, 2000))
    await authStore.logout()
    await router.push('/login')
  } catch (error) {
    console.error('Error changing password:', error)
    showError(error.response?.data?.detail || 'Failed to change password')
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

function initializeForm() {
  if (authStore.profile) {
    const { first_name, last_name, email, phone_number, date_of_birth } = authStore.profile
    
    profileForm.value.first_name = first_name
    profileForm.value.last_name = last_name
    profileForm.value.email = email
    profileForm.value.phone_number = phone_number
    profileForm.value.date_of_birth = formatDate(date_of_birth)

    // Set role-specific fields
    if (authStore.profile.role === 'student' && authStore.profile.student_details) {
      const { enrollment_number, department, date_of_admission, current_semester } = authStore.profile.student_details
      profileForm.value.student_details.enrollment_number = enrollment_number
      profileForm.value.student_details.department = department
      profileForm.value.student_details.date_of_admission = formatDate(date_of_admission)
      profileForm.value.student_details.current_semester = current_semester
    } else if (authStore.profile.role === 'faculty' && authStore.profile.faculty_details) {
      const { department, date_of_joining, qualification, specialization } = authStore.profile.faculty_details
      profileForm.value.faculty_details.department = department
      profileForm.value.faculty_details.date_of_joining = formatDate(date_of_joining)
      profileForm.value.faculty_details.qualification = qualification
      profileForm.value.faculty_details.specialization = specialization
    } else if (authStore.profile.role === 'hod' && authStore.profile.hod_details) {
      const { department, date_of_joining, qualification, experience_years } = authStore.profile.hod_details
      profileForm.value.hod_details.department = department
      profileForm.value.hod_details.date_of_joining = formatDate(date_of_joining)
      profileForm.value.hod_details.qualification = qualification
      profileForm.value.hod_details.experience_years = experience_years
    } else if (authStore.profile.role === 'principal') {
      // Initialize principal_details if null
      if (!authStore.profile.principal_details) {
        authStore.profile.principal_details = {
          qualification: '',
          experience_years: null,
          date_of_joining: null
        }
      }
      const { date_of_joining, qualification, experience_years } = authStore.profile.principal_details || {}
      profileForm.value.principal_details.date_of_joining = formatDate(date_of_joining)
      profileForm.value.principal_details.qualification = qualification || ''
      profileForm.value.principal_details.experience_years = experience_years || null
    } else if (authStore.profile.role === 'lab_assistant' && authStore.profile.lab_assistant_details) {
      const { department, date_of_joining, lab_type } = authStore.profile.lab_assistant_details
      profileForm.value.lab_assistant_details.department = department
      profileForm.value.lab_assistant_details.date_of_joining = formatDate(date_of_joining)
      profileForm.value.lab_assistant_details.lab_type = lab_type
    }
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