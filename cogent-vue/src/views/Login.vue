<template>
  <v-container fluid class="page-container fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="auth-card elevation-2">
          <v-card-title class="page-title">
            Login
          </v-card-title>

          <v-card-text>
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
                :items="roles"
                item-title="text"
                item-value="value"
                label="Role"
                prepend-icon="mdi-account"
                :rules="roleRules"
                required
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

const roleRules = [
  v => !!v || 'Role is required'
]

const roles = [
  { text: 'Principal', value: 'principal' },
  { text: 'HOD', value: 'hod' },
  { text: 'Faculty', value: 'faculty' },
  { text: 'Lab Assistant', value: 'lab_assistant' },
  { text: 'Student', value: 'student' }
]

const handleSubmit = async () => {
  if (!form.value.validate()) return

  loading.value = true
  try {
    await authStore.login({
      email: email.value,
      password: password.value,
      role: role.value
    })
    router.push(authStore.defaultRoute)
  } catch (error) {
    console.error('Login failed:', error)
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
