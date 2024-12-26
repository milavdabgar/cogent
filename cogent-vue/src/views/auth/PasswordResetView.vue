<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center py-4">
            {{ hasToken ? 'Reset Your Password' : 'Request Password Reset' }}
          </v-card-title>
          
          <v-card-text>
            <!-- Request Password Reset Form -->
            <v-form
              v-if="!hasToken"
              @submit.prevent="handleRequestReset"
              v-model="requestForm.valid"
            >
              <v-text-field
                v-model="requestForm.email"
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
                :loading="profileStore.loading"
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
                v-model="resetForm.new_password"
                label="New Password"
                type="password"
                :rules="[
                  v => !!v || 'New password is required',
                  v => v.length >= 8 || 'Password must be at least 8 characters'
                ]"
                required
              />
              
              <v-text-field
                v-model="resetForm.confirm_password"
                label="Confirm Password"
                type="password"
                :rules="[
                  v => !!v || 'Please confirm your password',
                  v => v === resetForm.new_password || 'Passwords must match'
                ]"
                required
              />
              
              <v-btn
                color="primary"
                type="submit"
                block
                class="mt-4"
                :loading="profileStore.loading"
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
import { useProfileStore } from '@/stores/profile'

const route = useRoute()
const router = useRouter()
const profileStore = useProfileStore()

const hasToken = computed(() => !!route.query.token)

const requestForm = ref({
  valid: true,
  email: ''
})

const resetForm = ref({
  valid: true,
  new_password: '',
  confirm_password: ''
})

const snackbar = ref({
  show: false,
  color: 'success',
  text: ''
})

async function handleRequestReset() {
  try {
    await profileStore.requestPasswordReset(requestForm.value.email)
    showSuccess('If the email exists, you will receive password reset instructions')
    requestForm.value.email = ''
  } catch (error) {
    showError('Failed to request password reset')
  }
}

async function handleResetPassword() {
  try {
    await profileStore.confirmPasswordReset(
      route.query.token,
      resetForm.value.new_password,
      resetForm.value.confirm_password
    )
    showSuccess('Password reset successfully')
    router.push({ name: 'login' })
  } catch (error) {
    showError('Failed to reset password')
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
