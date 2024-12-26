<template>
  <v-container fluid class="fill-height login-container">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-card-title class="text-h5 text-center py-4">
            Sign Up
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="handleSubmit">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="firstName"
                    label="First Name"
                    prepend-icon="mdi-account"
                    :rules="nameRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="lastName"
                    label="Last Name"
                    prepend-icon="mdi-account"
                    :rules="nameRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-text-field
                v-model="email"
                label="Email"
                prepend-icon="mdi-email"
                :rules="emailRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                :rules="passwordRules"
                @click:append="showPassword = !showPassword"
                required
              ></v-text-field>

              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                prepend-icon="mdi-lock"
                :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showConfirmPassword ? 'text' : 'password'"
                :rules="[...passwordRules, passwordMatch]"
                @click:append="showConfirmPassword = !showConfirmPassword"
                required
              ></v-text-field>

              <v-select
                v-model="role"
                :items="roles"
                label="Role"
                prepend-icon="mdi-account-group"
                :rules="roleRules"
                required
              ></v-select>

              <div v-if="role === 'student'">
                <v-text-field
                  v-model="enrollmentNumber"
                  label="Enrollment Number"
                  prepend-icon="mdi-identifier"
                  :rules="enrollmentRules"
                  required
                ></v-text-field>
                
                <v-select
                  v-model="department"
                  :items="departments"
                  label="Department"
                  prepend-icon="mdi-domain"
                  :rules="departmentRules"
                  required
                ></v-select>

                <v-select
                  v-model="currentSemester"
                  :items="semesters"
                  label="Current Semester"
                  prepend-icon="mdi-calendar"
                  :rules="semesterRules"
                  required
                ></v-select>
              </div>
            </v-form>
          </v-card-text>
          <v-card-actions class="px-4 pb-4">
            <v-btn
              color="primary"
              block
              :loading="loading"
              :disabled="!valid"
              @click="handleSubmit"
            >
              Sign Up
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center pt-0">
            Already have an account?
            <v-btn variant="text" to="/login" color="primary">
              Login
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          color="white"
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('')
const enrollmentNumber = ref('')
const department = ref('')
const currentSemester = ref(null)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const nameRules = [
  v => !!v || 'Name is required',
  v => v.length <= 50 || 'Name must be less than 50 characters'
]

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
const departmentRules = [v => !role.value || role.value !== 'student' || !!v || 'Department is required']
const semesterRules = [v => !role.value || role.value !== 'student' || !!v || 'Semester is required']

const roles = ['student', 'faculty', 'hod', 'lab_assistant']
const departments = ['Computer Science', 'Information Technology', 'Electronics', 'Mechanical']
const semesters = Array.from({ length: 8 }, (_, i) => i + 1)

const handleSubmit = async () => {
  if (!form.value.validate()) return

  loading.value = true
  try {
    const userData = {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      role: role.value
    }

    if (role.value === 'student') {
      userData.student_details = {
        enrollment_number: enrollmentNumber.value,
        department: department.value,
        current_semester: currentSemester.value
      }
    }

    await authStore.signup(userData)
    snackbar.value = {
      show: true,
      text: 'Account created successfully! Please login.',
      color: 'success'
    }
    router.push('/login')
  } catch (error) {
    snackbar.value = {
      show: true,
      text: error.response?.data?.detail || 'Failed to create account',
      color: 'error'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background-color: #1976d2;
  padding: 0;
  margin: 0;
  min-height: 100vh;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
}

.v-row {
  margin: 0;
  width: 100%;
}

.v-col {
  padding: 12px;
}

.v-card {
  width: 100%;
  margin: auto;
}
</style>
