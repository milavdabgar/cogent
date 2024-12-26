<template>
  <div class="page-container">
    <div class="form-wrapper">
      <v-card class="signup-card">
        <v-card-title class="text-center text-h5 pt-4">
          Sign Up
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid" @submit.prevent="handleSubmit">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="firstName"
                  label="First Name"
                  :rules="nameRules"
                  prepend-icon="mdi-account"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="lastName"
                  label="Last Name"
                  :rules="nameRules"
                  prepend-icon="mdi-account"
                  required
                ></v-text-field>
              </v-col>
            </v-row>

            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              :rules="emailRules"
              prepend-icon="mdi-email"
              required
            ></v-text-field>

            <v-text-field
              v-model="phoneNumber"
              label="Phone Number"
              :rules="phoneNumberRules"
              prepend-icon="mdi-phone"
              required
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Password"
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
              :rules="passwordRules"
              prepend-icon="mdi-lock"
              required
            ></v-text-field>

            <v-text-field
              v-model="confirmPassword"
              label="Confirm Password"
              :type="showConfirmPassword ? 'text' : 'password'"
              :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showConfirmPassword = !showConfirmPassword"
              :rules="[...passwordRules, passwordMatch]"
              prepend-icon="mdi-lock"
              required
            ></v-text-field>

            <v-text-field
              v-model="dateOfBirth"
              type="date"
              label="Date of Birth"
              prepend-icon="mdi-cake-variant"
              :rules="dateOfBirthRules"
              required
            ></v-text-field>

            <v-select
              v-model="role"
              :items="roles"
              item-title="text"
              item-value="value"
              label="Role"
              prepend-icon="mdi-account-group"
              :rules="roleRules"
              required
            ></v-select>

            <!-- Department field for roles that need it -->
            <div v-if="['student', 'faculty', 'hod', 'lab_assistant'].includes(role)">
              <v-select
                v-model="department"
                :items="departments"
                label="Department"
                prepend-icon="mdi-domain"
                :rules="departmentRules"
                required
              ></v-select>
            </div>

            <!-- Student specific fields -->
            <div v-if="role === 'student'" class="auth-section">
              <v-text-field
                v-model="enrollmentNumber"
                label="Enrollment Number"
                prepend-icon="mdi-identifier"
                :rules="enrollmentRules"
                required
              ></v-text-field>

              <v-select
                v-model="currentSemester"
                :items="semesters"
                label="Current Semester"
                prepend-icon="mdi-calendar"
                :rules="semesterRules"
                required
              ></v-select>

              <v-text-field
                v-model="dateOfAdmission"
                type="date"
                label="Date of Admission"
                prepend-icon="mdi-calendar"
                :rules="dateRules"
                required
              ></v-text-field>
            </div>

            <!-- Faculty specific fields -->
            <div v-if="role === 'faculty'" class="auth-section">
              <v-text-field
                v-model="qualification"
                label="Qualification"
                prepend-icon="mdi-school"
                :rules="qualificationRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="specialization"
                label="Specialization"
                prepend-icon="mdi-book-open-variant"
                :rules="specializationRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="dateOfJoining"
                type="date"
                label="Date of Joining"
                prepend-icon="mdi-calendar"
                :rules="dateRules"
                required
              ></v-text-field>
            </div>

            <!-- HOD specific fields -->
            <div v-if="role === 'hod'" class="auth-section">
              <v-text-field
                v-model="qualification"
                label="Qualification"
                prepend-icon="mdi-school"
                :rules="qualificationRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="experienceYears"
                label="Years of Experience"
                type="number"
                prepend-icon="mdi-clock-outline"
                :rules="experienceRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="dateOfJoining"
                type="date"
                label="Date of Joining"
                prepend-icon="mdi-calendar"
                :rules="dateRules"
                required
              ></v-text-field>
            </div>

            <!-- Principal specific fields -->
            <div v-if="role === 'principal'" class="auth-section">
              <v-text-field
                v-model="qualification"
                label="Qualification"
                prepend-icon="mdi-school"
                :rules="qualificationRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="experienceYears"
                label="Years of Experience"
                type="number"
                prepend-icon="mdi-clock-outline"
                :rules="experienceRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="dateOfJoining"
                type="date"
                label="Date of Joining"
                prepend-icon="mdi-calendar"
                :rules="dateRules"
                required
              ></v-text-field>
            </div>

            <!-- Lab Assistant specific fields -->
            <div v-if="role === 'lab_assistant'" class="auth-section">
              <v-text-field
                v-model="labType"
                label="Lab Type"
                prepend-icon="mdi-flask"
                :rules="labTypeRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="dateOfJoining"
                type="date"
                label="Date of Joining"
                prepend-icon="mdi-calendar"
                :rules="dateRules"
                required
              ></v-text-field>
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions class="px-4 pb-4">
          <v-btn
            color="primary"
            type="submit"
            block
            :loading="loading"
            :disabled="!valid"
            @click="handleSubmit"
          >
            Sign Up
          </v-btn>
        </v-card-actions>

        <v-card-text class="text-center pt-0">
          <span class="text-grey">Already have an account? </span>
          <router-link to="/login" class="auth-link">Login</router-link>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const firstName = ref('')
const lastName = ref('')
const role = ref('')
const dateOfBirth = ref('')
const phoneNumber = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const enrollmentNumber = ref('')
const department = ref('')
const currentSemester = ref(null)
const qualification = ref('')
const specialization = ref('')
const experienceYears = ref(null)
const dateOfJoining = ref('')
const dateOfAdmission = ref('')
const labType = ref('')

const roles = [
  { text: 'Principal', value: 'principal' },
  { text: 'HOD', value: 'hod' },
  { text: 'Faculty', value: 'faculty' },
  { text: 'Lab Assistant', value: 'lab_assistant' },
  { text: 'Student', value: 'student' }
]

const departments = [
  'Computer Science',
  'Electronics',
  'Mechanical',
  'Civil',
  'Electrical'
]

const semesters = Array.from({ length: 8 }, (_, i) => i + 1)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const nameRules = [v => !!v || 'Name is required']
const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Email must be valid'
]
const passwordRules = [
  v => !!v || 'Password is required',
  v => v.length >= 6 || 'Password must be at least 6 characters'
]
const passwordMatch = () => password.value === confirmPassword.value || 'Passwords must match'
const roleRules = [v => !!v || 'Role is required']
const enrollmentRules = [v => !role.value || role.value !== 'student' || !!v || 'Enrollment number is required']
const departmentRules = [v => !role.value || !['student', 'faculty', 'hod', 'lab_assistant'].includes(role.value) || !!v || 'Department is required']
const semesterRules = [v => !role.value || role.value !== 'student' || !!v || 'Semester is required']
const qualificationRules = [v => !role.value || !['principal', 'hod', 'faculty'].includes(role.value) || !!v || 'Qualification is required']
const specializationRules = [v => !role.value || role.value !== 'faculty' || !!v || 'Specialization is required']
const experienceRules = [v => !role.value || !['principal', 'hod'].includes(role.value) || !!v || 'Years of experience is required']
const dateRules = [v => !!v || 'Date is required']
const labTypeRules = [v => !role.value || role.value !== 'lab_assistant' || !!v || 'Lab type is required']
const dateOfBirthRules = [
  v => !!v || 'Date of birth is required',
  v => {
    if (!v) return true
    const birthDate = new Date(v)
    const today = new Date()
    const age = today.getFullYear() - birthDate.getFullYear()
    return age >= 16 || 'Must be at least 16 years old'
  }
]
const phoneNumberRules = [
  v => !!v || 'Phone number is required',
  v => /^\d{10}$/.test(v) || 'Phone number must be 10 digits'
]

const formatDate = (date) => {
  if (!date) return null
  return new Date(date).toISOString().split('T')[0]
}

const handleSubmit = async () => {
  if (!form.value.validate()) return

  loading.value = true
  
  try {
    const userData = {
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      role: role.value,
      phone_number: phoneNumber.value,
      date_of_birth: formatDate(dateOfBirth.value),
      is_active: true
    }

    // Add role-specific details
    if (role.value === 'student') {
      userData.student_details = {
        enrollment_number: enrollmentNumber.value,
        department: department.value,
        date_of_admission: formatDate(dateOfAdmission.value),
        current_semester: parseInt(currentSemester.value)
      }
    } else if (role.value === 'faculty') {
      userData.faculty_details = {
        department: department.value,
        date_of_joining: formatDate(dateOfJoining.value),
        qualification: qualification.value,
        specialization: specialization.value
      }
    } else if (role.value === 'hod') {
      userData.hod_details = {
        department: department.value,
        date_of_joining: formatDate(dateOfJoining.value),
        qualification: qualification.value,
        experience_years: parseInt(experienceYears.value)
      }
    } else if (role.value === 'principal') {
      userData.principal_details = {
        date_of_joining: formatDate(dateOfJoining.value),
        qualification: qualification.value,
        experience_years: parseInt(experienceYears.value)
      }
    } else if (role.value === 'lab_assistant') {
      userData.lab_assistant_details = {
        department: department.value,
        date_of_joining: formatDate(dateOfJoining.value),
        lab_type: labType.value
      }
    }

    await authStore.signup(userData)
    router.push('/login')
    snackbar.value = {
      show: true,
      color: 'success',
      text: 'Successfully signed up! Please login.'
    }
  } catch (error) {
    console.error('Signup error:', error)
    snackbar.value = {
      show: true,
      color: 'error',
      text: error.response?.data?.detail || 'Failed to sign up. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-container {
  background-color: #f5f5f5;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.form-wrapper {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.signup-card {
  width: 100%;
  padding: 1rem;
}

@media (max-width: 600px) {
  .page-container {
    padding: 1rem;
  }
}
</style>
