<template>
  <v-container fluid class="page-container fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="auth-card elevation-2">
          <v-card-title class="page-title">
            Login
          </v-card-title>

          <v-card-text>
            <v-alert
              v-if="errorMessage"
              type="error"
              variant="tonal"
              closable
              class="mb-4"
              @click:close="errorMessage = ''"
            >
              {{ errorMessage }}
            </v-alert>

            <v-form ref="form" v-model="valid" @submit.prevent="handleSubmit" class="form-container">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="emailRules"
                prepend-icon="mdi-email"
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

              <v-select
                v-model="role"
                :items="[
                  { title: 'DTE Admin', value: 'DTE_ADMIN' },
                  { title: 'GTU Admin', value: 'GTU_ADMIN' },
                  { title: 'Principal', value: 'PRINCIPAL' },
                  { title: 'HOD', value: 'HOD' },
                  { title: 'Faculty', value: 'FACULTY' },
                  { title: 'Lab Assistant', value: 'LAB_ASSISTANT' },
                  { title: 'Student', value: 'STUDENT' }
                ]"
                item-title="title"
                item-value="value"
                label="Role"
                prepend-icon="mdi-account"
                required
                :rules="[v => !!v || 'Role is required']"
              ></v-select>
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
              Login
            </v-btn>
          </v-card-actions>

          <v-card-text class="text-center pt-0">
            <span class="text-grey">Don't have an account? </span>
            <router-link to="/signup" class="auth-link">Sign up</router-link>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const errorMessage = ref('')
const snackbar = ref({ show: false, text: '', color: 'success' })

const email = ref('')
const password = ref('')
const role = ref('')

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Email must be valid'
]

const passwordRules = [
  v => !!v || 'Password is required',
  v => v.length >= 6 || 'Password must be at least 6 characters'
]

const handleSubmit = async () => {
  if (!form.value.validate()) return

  loading.value = true
  errorMessage.value = ''
  
  try {
    await authStore.login({
      email: email.value,
      password: password.value,
      role: role.value
    })
    snackbar.value = {
      show: true,
      text: 'Login successful!',
      color: 'success'
    }
    router.push(authStore.defaultRoute)
  } catch (error) {
    console.error('Login failed:', error)
    if (error.response?.status === 401) {
      errorMessage.value = 'Invalid email, password, or role. Please check your credentials.'
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'An error occurred during login. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-container {
  background-color: #f5f5f5;
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

.auth-card {
  width: 100%;
  max-width: 400px;
  margin: auto;
}

.form-container {
  padding: 20px;
}

.auth-link {
  text-decoration: none;
}
</style>
