<template>
  <v-container fluid class="fill-height pa-0 ma-0 home-container">
    <v-row align="center" justify="center" class="fill-height ma-0">
      <v-col cols="12" class="fill-height d-flex align-center justify-center pa-4">
        <v-card class="mx-auto pa-8 rounded-lg elevation-10" max-width="600">
          <h1 class="text-h2 font-weight-bold mb-4">Welcome to Cogent</h1>
          <p class="text-body-1 mb-8">
            Your comprehensive college portal for managing academic activities.
          </p>
          <v-btn
            color="primary"
            size="x-large"
            to="/login"
            class="mx-2"
            elevation="2"
          >
            Login
          </v-btn>
          <v-btn
            color="secondary"
            size="x-large"
            to="/signup"
            class="mx-2"
            elevation="2"
          >
            Sign Up
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// Home page is simple and just provides navigation to login/signup
</script>

<style scoped>
.home-container {
  background: linear-gradient(135deg, #1867C0 0%, #5CBBF6 100%);
  min-height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.v-container {
  max-width: none !important;
}

.v-row {
  margin: 0 !important;
}
</style>
