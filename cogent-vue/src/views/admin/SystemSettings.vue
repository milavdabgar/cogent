<template>
  <div class="system-settings">
    <v-container>
      <!-- Header -->
      <v-row class="mb-4">
        <v-col cols="12">
          <h2 class="text-h4">System Settings</h2>
        </v-col>
      </v-row>

      <!-- Settings Sections -->
      <v-row>
        <v-col cols="12" md="8">
          <!-- General Settings -->
          <v-card class="mb-4">
            <v-card-title>General Settings</v-card-title>
            <v-card-text>
              <v-form ref="generalForm" v-model="generalValid">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="settings.systemName"
                      label="System Name"
                      :rules="[v => !!v || 'System name is required']"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="settings.contactEmail"
                      label="Contact Email"
                      type="email"
                      :rules="emailRules"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="settings.academicYear"
                      :items="academicYears"
                      label="Current Academic Year"
                      required
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="settings.currentSemester"
                      :items="[1,2,3,4,5,6,7,8]"
                      label="Current Semester"
                      required
                    ></v-select>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                :loading="saving"
                :disabled="!generalValid || saving"
                @click="saveGeneralSettings"
              >
                Save General Settings
              </v-btn>
            </v-card-actions>
          </v-card>

          <!-- Email Settings -->
          <v-card class="mb-4">
            <v-card-title>Email Settings</v-card-title>
            <v-card-text>
              <v-form ref="emailForm" v-model="emailValid">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="settings.smtpHost"
                      label="SMTP Host"
                      :rules="[v => !!v || 'SMTP host is required']"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="settings.smtpPort"
                      label="SMTP Port"
                      type="number"
                      :rules="[v => !!v || 'SMTP port is required']"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="settings.smtpUsername"
                      label="SMTP Username"
                      :rules="[v => !!v || 'SMTP username is required']"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="settings.smtpPassword"
                      label="SMTP Password"
                      type="password"
                      :rules="[v => !!v || 'SMTP password is required']"
                      required
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                class="mr-2"
                :loading="testing"
                :disabled="!emailValid || testing"
                @click="testEmailSettings"
              >
                Test Connection
              </v-btn>
              <v-btn
                color="primary"
                :loading="saving"
                :disabled="!emailValid || saving"
                @click="saveEmailSettings"
              >
                Save Email Settings
              </v-btn>
            </v-card-actions>
          </v-card>

          <!-- Backup Settings -->
          <v-card class="mb-4">
            <v-card-title>Database Backup</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="settings.backupFrequency"
                    :items="[
                      { title: 'Daily', value: 'daily' },
                      { title: 'Weekly', value: 'weekly' },
                      { title: 'Monthly', value: 'monthly' }
                    ]"
                    label="Backup Frequency"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="settings.backupRetentionDays"
                    label="Retention Period (days)"
                    type="number"
                    min="1"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="warning"
                class="mr-2"
                :loading="backingUp"
                @click="backupNow"
              >
                Backup Now
              </v-btn>
              <v-btn
                color="primary"
                :loading="saving"
                @click="saveBackupSettings"
              >
                Save Backup Settings
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- System Info -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>System Information</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-information</v-icon>
                  </template>
                  <v-list-item-title>Version</v-list-item-title>
                  <v-list-item-subtitle>{{ systemInfo.version }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-database</v-icon>
                  </template>
                  <v-list-item-title>Database Size</v-list-item-title>
                  <v-list-item-subtitle>{{ systemInfo.dbSize }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-calendar</v-icon>
                  </template>
                  <v-list-item-title>Last Backup</v-list-item-title>
                  <v-list-item-subtitle>{{ systemInfo.lastBackup }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-account-group</v-icon>
                  </template>
                  <v-list-item-title>Total Users</v-list-item-title>
                  <v-list-item-subtitle>{{ systemInfo.totalUsers }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Snackbar for notifications -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'SystemSettings',

  setup() {
    // Data
    const settings = ref({
      systemName: '',
      contactEmail: '',
      academicYear: '',
      currentSemester: 1,
      smtpHost: '',
      smtpPort: 587,
      smtpUsername: '',
      smtpPassword: '',
      backupFrequency: 'daily',
      backupRetentionDays: 30
    })

    const systemInfo = ref({
      version: '1.0.0',
      dbSize: '0 MB',
      lastBackup: 'Never',
      totalUsers: 0
    })

    const generalValid = ref(false)
    const emailValid = ref(false)
    const generalForm = ref(null)
    const emailForm = ref(null)
    const saving = ref(false)
    const testing = ref(false)
    const backingUp = ref(false)

    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    // Current year for academic year generation
    const currentYear = new Date().getFullYear()
    const academicYears = [
      `${currentYear-1}-${currentYear}`,
      `${currentYear}-${currentYear+1}`,
      `${currentYear+1}-${currentYear+2}`
    ]

    const emailRules = [
      v => !!v || 'Email is required',
      v => /.+@.+\..+/.test(v) || 'Email must be valid'
    ]

    // Methods
    const fetchSettings = async () => {
      try {
        const response = await axios.get('/api/v1/admin/settings/')
        settings.value = { ...settings.value, ...response.data }
      } catch (error) {
        showError('Error fetching settings')
        console.error('Error:', error)
      }
    }

    const fetchSystemInfo = async () => {
      try {
        const response = await axios.get('/api/v1/admin/system-info/')
        systemInfo.value = response.data
      } catch (error) {
        showError('Error fetching system information')
        console.error('Error:', error)
      }
    }

    const saveGeneralSettings = async () => {
      if (!generalForm.value?.validate()) return

      saving.value = true
      try {
        await axios.put('/api/v1/admin/settings/general', {
          systemName: settings.value.systemName,
          contactEmail: settings.value.contactEmail,
          academicYear: settings.value.academicYear,
          currentSemester: settings.value.currentSemester
        })
        showSuccess('General settings saved successfully')
      } catch (error) {
        showError('Error saving general settings')
        console.error('Error:', error)
      } finally {
        saving.value = false
      }
    }

    const saveEmailSettings = async () => {
      if (!emailForm.value?.validate()) return

      saving.value = true
      try {
        await axios.put('/api/v1/admin/settings/email', {
          smtpHost: settings.value.smtpHost,
          smtpPort: settings.value.smtpPort,
          smtpUsername: settings.value.smtpUsername,
          smtpPassword: settings.value.smtpPassword
        })
        showSuccess('Email settings saved successfully')
      } catch (error) {
        showError('Error saving email settings')
        console.error('Error:', error)
      } finally {
        saving.value = false
      }
    }

    const testEmailSettings = async () => {
      if (!emailForm.value?.validate()) return

      testing.value = true
      try {
        await axios.post('/api/v1/admin/settings/email/test', {
          smtpHost: settings.value.smtpHost,
          smtpPort: settings.value.smtpPort,
          smtpUsername: settings.value.smtpUsername,
          smtpPassword: settings.value.smtpPassword
        })
        showSuccess('Email test successful')
      } catch (error) {
        showError('Email test failed')
        console.error('Error:', error)
      } finally {
        testing.value = false
      }
    }

    const saveBackupSettings = async () => {
      saving.value = true
      try {
        await axios.put('/api/v1/admin/settings/backup', {
          backupFrequency: settings.value.backupFrequency,
          backupRetentionDays: settings.value.backupRetentionDays
        })
        showSuccess('Backup settings saved successfully')
      } catch (error) {
        showError('Error saving backup settings')
        console.error('Error:', error)
      } finally {
        saving.value = false
      }
    }

    const backupNow = async () => {
      backingUp.value = true
      try {
        await axios.post('/api/v1/admin/backup/')
        showSuccess('Backup completed successfully')
        await fetchSystemInfo() // Refresh system info to show new backup time
      } catch (error) {
        showError('Error creating backup')
        console.error('Error:', error)
      } finally {
        backingUp.value = false
      }
    }

    const showSuccess = (text) => {
      snackbar.value = {
        show: true,
        text,
        color: 'success'
      }
    }

    const showError = (text) => {
      snackbar.value = {
        show: true,
        text,
        color: 'error'
      }
    }

    // Lifecycle hooks
    onMounted(() => {
      fetchSettings()
      fetchSystemInfo()
    })

    return {
      settings,
      systemInfo,
      generalValid,
      emailValid,
      generalForm,
      emailForm,
      saving,
      testing,
      backingUp,
      snackbar,
      academicYears,
      emailRules,
      saveGeneralSettings,
      saveEmailSettings,
      testEmailSettings,
      saveBackupSettings,
      backupNow
    }
  }
}
</script>

<style scoped>
.system-settings {
  padding: 20px;
}
</style>
