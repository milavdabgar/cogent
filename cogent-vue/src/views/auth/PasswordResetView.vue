<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center py-4">
            {{ step === 1 ? 'Request Password Reset' : 'Reset Your Password' }}
          </v-card-title>
          
          <v-card-text>
            <!-- Request Password Reset Form -->
            <v-form
              v-if="step === 1"
              @submit.prevent="handleRequestReset"
              v-model="requestForm.valid"
            >
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="[
                  v => !!v || 'Email is required',
                  v => /.+@.+\..+/.test(v) || 'Email must be valid'
                ]"
                required
              />
              
              <v-btn
                color="primary"
                type="submit"
                block
                class="mt-4"
                :loading="loading"
                :disabled="!requestForm.valid"
              >
                Request Reset
              </v-btn>
            </v-form>
            
            <!-- Reset Password Form -->
            <v-form
              v-else
              @submit.prevent="handleResetPassword"
              v-model="resetForm.valid"
            >
              <v-text-field
                v-model="newPassword"
                label="New Password"
                type="password"
                :rules="[
                  v => !!v || 'New password is required',
                  v => v.length >= 8 || 'Password must be at least 8 characters'
                ]"
                required
              />
              
              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                type="password"
                :rules="[
                  v => !!v || 'Please confirm your password',
                  v => v === newPassword || 'Passwords must match'
                ]"
                required
              />
              
              <v-btn
                color="primary"
                type="submit"
                block
                class="mt-4"
                :loading="loading"
                :disabled="!resetForm.valid"
              >
                Reset Password
              </v-btn>
            </v-form>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer />
            <v-btn
              variant="text"
              :to="{ name: 'login' }"
              class="mb-4"
            >
              Back to Login
            </v-btn>
            <v-spacer />
          </v-card-actions>
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
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const token = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const step = ref(1)
const error = ref('')
const success = ref('')
const loading = ref(false)

const requestForm = ref({
  valid: true
})

const resetForm = ref({
  valid: true
})

const snackbar = ref({
  show: false,
  color: 'success',
  text: ''
})

async function handleRequestReset() {
  try {
    loading.value = true
    error.value = ''
    await authStore.requestPasswordReset(email.value)
    success.value = 'Password reset link has been sent to your email'
    step.value = 2
  } catch (err) {
    error.value = err.message || 'Failed to request password reset'
  } finally {
    loading.value = false
  }
}

async function handleResetPassword() {
  try {
    loading.value = true
    error.value = ''
    await authStore.confirmPasswordReset(token.value, newPassword.value, confirmPassword.value)
    success.value = 'Password has been reset successfully'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    error.value = err.message || 'Failed to reset password'
  } finally {
    loading.value = false
  }
}

function showSuccess(text) {
  snackbar.value = {
    show: true,
    color: 'success',
    text
  }
}

function showError(text) {
  snackbar.value = {
    show: true,
    color: 'error',
    text
  }
}
</script>
