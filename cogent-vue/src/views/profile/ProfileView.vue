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
                        <v-menu
                          v-if="isEditing"
                          v-model="dateAdmissionMenu"
                          :close-on-content-click="false"
                        >
                          <template v-slot:activator="{ props }">
                            <v-text-field
                              v-model="formattedDateOfAdmission"
                              label="Date of Admission"
                              readonly
                              v-bind="props"
                              variant="outlined"
                              :class="{ 'editable': isEditing }"
                              prepend-icon="mdi-calendar"
                            />
                          </template>
                          <v-date-picker
                            v-model="profileForm.student_details.date_of_admission"
                            @update:model-value="dateAdmissionMenu = false"
                          />
                        </v-menu>
                        <v-text-field
                          v-else
                          v-model="formattedDateOfAdmission"
                          label="Date of Admission"
                          readonly
                          variant="outlined"
                        />
                      </v-col>
                    </template>

                    <template v-if="profileStore.profile?.role === 'faculty'">
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
                        <v-menu
                          v-if="isEditing"
                          v-model="dateJoiningMenu"
                          :close-on-content-click="false"
                        >
                          <template v-slot:activator="{ props }">
                            <v-text-field
                              v-model="formattedDateOfJoining"
                              label="Date of Joining"
                              readonly
                              v-bind="props"
                              variant="outlined"
                              :class="{ 'editable': isEditing }"
                              prepend-icon="mdi-calendar"
                            />
                          </template>
                          <v-date-picker
                            v-model="profileForm.faculty_details.date_of_joining"
                            @update:model-value="dateJoiningMenu = false"
                          />
                        </v-menu>
                        <v-text-field
                          v-else
                          v-model="formattedDateOfJoining"
                          label="Date of Joining"
                          readonly
                          variant="outlined"
                        />
                      </v-col>
                    </template>

                    <template v-if="profileStore.profile?.role === 'hod'">
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
                        <v-menu
                          v-if="isEditing"
                          v-model="dateJoiningMenu"
                          :close-on-content-click="false"
                        >
                          <template v-slot:activator="{ props }">
                            <v-text-field
                              v-model="formattedDateOfJoining"
                              label="Date of Joining"
                              readonly
                              v-bind="props"
                              variant="outlined"
                              :class="{ 'editable': isEditing }"
                              prepend-icon="mdi-calendar"
                            />
                          </template>
                          <v-date-picker
                            v-model="profileForm.hod_details.date_of_joining"
                            @update:model-value="dateJoiningMenu = false"
                          />
                        </v-menu>
                        <v-text-field
                          v-else
                          v-model="formattedDateOfJoining"
                          label="Date of Joining"
                          readonly
                          variant="outlined"
                        />
                      </v-col>
                    </template>

                    <template v-if="profileStore.profile?.role === 'principal'">
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
                        <v-menu
                          v-if="isEditing"
                          v-model="dateJoiningMenu"
                          :close-on-content-click="false"
                        >
                          <template v-slot:activator="{ props }">
                            <v-text-field
                              v-model="formattedDateOfJoining"
                              label="Date of Joining"
                              readonly
                              v-bind="props"
                              variant="outlined"
                              :class="{ 'editable': isEditing }"
                              prepend-icon="mdi-calendar"
                            />
                          </template>
                          <v-date-picker
                            v-model="profileForm.principal_details.date_of_joining"
                            @update:model-value="dateJoiningMenu = false"
                          />
                        </v-menu>
                        <v-text-field
                          v-else
                          v-model="formattedDateOfJoining"
                          label="Date of Joining"
                          readonly
                          variant="outlined"
                        />
                      </v-col>
                    </template>

                    <template v-if="profileStore.profile?.role === 'lab_assistant'">
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
                        <v-menu
                          v-if="isEditing"
                          v-model="dateJoiningMenu"
                          :close-on-content-click="false"
                        >
                          <template v-slot:activator="{ props }">
                            <v-text-field
                              v-model="formattedDateOfJoining"
                              label="Date of Joining"
                              readonly
                              v-bind="props"
                              variant="outlined"
                              :class="{ 'editable': isEditing }"
                              prepend-icon="mdi-calendar"
                            />
                          </template>
                          <v-date-picker
                            v-model="profileForm.lab_assistant_details.date_of_joining"
                            @update:model-value="dateJoiningMenu = false"
                          />
                        </v-menu>
                        <v-text-field
                          v-else
                          v-model="formattedDateOfJoining"
                          label="Date of Joining"
                          readonly
                          variant="outlined"
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
const dateJoiningMenu = ref(false)
const dateAdmissionMenu = ref(false)

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

// Format date for display
const formattedDateOfBirth = computed(() => formatDate(profileForm.value.date_of_birth))
const formattedDateOfJoining = computed(() => {
  const role = profileStore.profile?.role
  if (!role) return ''
  
  let date = ''
  switch (role) {
    case 'faculty':
      date = profileForm.value.faculty_details.date_of_joining
      break
    case 'hod':
      date = profileForm.value.hod_details.date_of_joining
      break
    case 'principal':
      date = profileForm.value.principal_details.date_of_joining
      break
    case 'lab_assistant':
      date = profileForm.value.lab_assistant_details.date_of_joining
      break
  }
  return formatDate(date)
})
const formattedDateOfAdmission = computed(() => formatDate(profileForm.value.student_details.date_of_admission))

// Date formatter
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

onMounted(async () => {
  try {
    await profileStore.fetchProfile()
    if (profileStore.profile) {
      // Set basic fields
      const { first_name, last_name, email, phone_number, date_of_birth } = profileStore.profile
      profileForm.value.first_name = first_name
      profileForm.value.last_name = last_name
      profileForm.value.email = email
      profileForm.value.phone_number = phone_number
      profileForm.value.date_of_birth = date_of_birth

      // Set role-specific fields
      if (profileStore.profile.role === 'student' && profileStore.profile.student_details) {
        const { enrollment_number, department, date_of_admission, current_semester } = profileStore.profile.student_details
        profileForm.value.student_details.enrollment_number = enrollment_number
        profileForm.value.student_details.department = department
        profileForm.value.student_details.date_of_admission = date_of_admission
        profileForm.value.student_details.current_semester = current_semester
      } else if (profileStore.profile.role === 'faculty' && profileStore.profile.faculty_details) {
        const { department, date_of_joining, qualification, specialization } = profileStore.profile.faculty_details
        profileForm.value.faculty_details.department = department
        profileForm.value.faculty_details.date_of_joining = date_of_joining
        profileForm.value.faculty_details.qualification = qualification
        profileForm.value.faculty_details.specialization = specialization
      } else if (profileStore.profile.role === 'hod' && profileStore.profile.hod_details) {
        const { department, date_of_joining, qualification, experience_years } = profileStore.profile.hod_details
        profileForm.value.hod_details.department = department
        profileForm.value.hod_details.date_of_joining = date_of_joining
        profileForm.value.hod_details.qualification = qualification
        profileForm.value.hod_details.experience_years = experience_years
      } else if (profileStore.profile.role === 'principal' && profileStore.profile.principal_details) {
        const { date_of_joining, qualification, experience_years } = profileStore.profile.principal_details
        profileForm.value.principal_details.date_of_joining = date_of_joining
        profileForm.value.principal_details.qualification = qualification
        profileForm.value.principal_details.experience_years = experience_years
      } else if (profileStore.profile.role === 'lab_assistant' && profileStore.profile.lab_assistant_details) {
        const { department, date_of_joining, lab_type } = profileStore.profile.lab_assistant_details
        profileForm.value.lab_assistant_details.department = department
        profileForm.value.lab_assistant_details.date_of_joining = date_of_joining
        profileForm.value.lab_assistant_details.lab_type = lab_type
      }
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
    showError('Failed to load profile')
  }
})

const toggleEditMode = () => {
  if (isEditing.value) {
    // Reset form when canceling edit
    if (profileStore.profile) {
      // Reset basic fields
      const { first_name, last_name, email, phone_number, date_of_birth } = profileStore.profile
      profileForm.value.first_name = first_name
      profileForm.value.last_name = last_name
      profileForm.value.email = email
      profileForm.value.phone_number = phone_number
      profileForm.value.date_of_birth = date_of_birth

      // Reset role-specific fields
      if (profileStore.profile.role === 'student' && profileStore.profile.student_details) {
        const { enrollment_number, department, date_of_admission, current_semester } = profileStore.profile.student_details
        profileForm.value.student_details.enrollment_number = enrollment_number
        profileForm.value.student_details.department = department
        profileForm.value.student_details.date_of_admission = date_of_admission
        profileForm.value.student_details.current_semester = current_semester
      } else if (profileStore.profile.role === 'faculty' && profileStore.profile.faculty_details) {
        const { department, date_of_joining, qualification, specialization } = profileStore.profile.faculty_details
        profileForm.value.faculty_details.department = department
        profileForm.value.faculty_details.date_of_joining = date_of_joining
        profileForm.value.faculty_details.qualification = qualification
        profileForm.value.faculty_details.specialization = specialization
      } else if (profileStore.profile.role === 'hod' && profileStore.profile.hod_details) {
        const { department, date_of_joining, qualification, experience_years } = profileStore.profile.hod_details
        profileForm.value.hod_details.department = department
        profileForm.value.hod_details.date_of_joining = date_of_joining
        profileForm.value.hod_details.qualification = qualification
        profileForm.value.hod_details.experience_years = experience_years
      } else if (profileStore.profile.role === 'principal' && profileStore.profile.principal_details) {
        const { date_of_joining, qualification, experience_years } = profileStore.profile.principal_details
        profileForm.value.principal_details.date_of_joining = date_of_joining
        profileForm.value.principal_details.qualification = qualification
        profileForm.value.principal_details.experience_years = experience_years
      } else if (profileStore.profile.role === 'lab_assistant' && profileStore.profile.lab_assistant_details) {
        const { department, date_of_joining, lab_type } = profileStore.profile.lab_assistant_details
        profileForm.value.lab_assistant_details.department = department
        profileForm.value.lab_assistant_details.date_of_joining = date_of_joining
        profileForm.value.lab_assistant_details.lab_type = lab_type
      }
    }
  }
  isEditing.value = !isEditing.value
}

const handleProfileUpdate = async () => {
  try {
    const updateData = {
      first_name: profileForm.value.first_name,
      last_name: profileForm.value.last_name,
      phone_number: profileForm.value.phone_number,
      date_of_birth: profileForm.value.date_of_birth
    }

    if (profileStore.profile?.role === 'student') {
      updateData.student_details = {
        enrollment_number: profileForm.value.student_details.enrollment_number,
        department: profileForm.value.student_details.department,
        date_of_admission: profileForm.value.student_details.date_of_admission,
        current_semester: profileForm.value.student_details.current_semester
      }
    } else if (profileStore.profile?.role === 'faculty') {
      updateData.faculty_details = {
        department: profileForm.value.faculty_details.department,
        date_of_joining: profileForm.value.faculty_details.date_of_joining,
        qualification: profileForm.value.faculty_details.qualification,
        specialization: profileForm.value.faculty_details.specialization
      }
    } else if (profileStore.profile?.role === 'hod') {
      updateData.hod_details = {
        department: profileForm.value.hod_details.department,
        date_of_joining: profileForm.value.hod_details.date_of_joining,
        qualification: profileForm.value.hod_details.qualification,
        experience_years: profileForm.value.hod_details.experience_years
      }
    } else if (profileStore.profile?.role === 'principal') {
      updateData.principal_details = {
        date_of_joining: profileForm.value.principal_details.date_of_joining,
        qualification: profileForm.value.principal_details.qualification,
        experience_years: profileForm.value.principal_details.experience_years
      }
    } else if (profileStore.profile?.role === 'lab_assistant') {
      updateData.lab_assistant_details = {
        department: profileForm.value.lab_assistant_details.department,
        date_of_joining: profileForm.value.lab_assistant_details.date_of_joining,
        lab_type: profileForm.value.lab_assistant_details.lab_type
      }
    }

    await profileStore.updateProfile(updateData)
    showSuccess('Profile updated successfully')
    isEditing.value = false
  } catch (error) {
    console.error('Error updating profile:', error)
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
    console.error('Error changing password:', error)
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