<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body p-4">
            <div class="text-center mb-4">
              <i class="bi bi-person-plus-fill text-primary" style="font-size: 3rem;"></i>
              <h2 class="mt-2">Register</h2>
              <p class="text-muted">Create your parking account</p>
            </div>

            <ErrorAlert :message="errorMessage" @clear="errorMessage = ''" />

            <!-- Success Message -->
            <div
              v-if="successMessage"
              class="alert alert-success alert-dismissible fade show"
              role="alert"
            >
              <i class="bi bi-check-circle-fill me-2"></i>
              {{ successMessage }}
              <button
                type="button"
                class="btn-close"
                @click="successMessage = ''"
                aria-label="Close"
              ></button>
            </div>

            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="form.username"
                  required
                  :disabled="isLoading"
                />
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="form.email"
                  required
                  :disabled="isLoading"
                />
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                  :disabled="isLoading"
                  minlength="6"
                />
                <div class="form-text">Password must be at least 6 characters long.</div>
              </div>
              
              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                Register
              </button>
            </form>

            <div class="text-center mt-3">
              <p class="mb-0">
                Already have an account?
                <router-link to="/login" class="text-decoration-none">Login here</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import ErrorAlert from '@/components/ErrorAlert.vue'

const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const form = reactive({
  username: '',
  email: '',
  password: ''
})

const handleRegister = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    await authStore.register(form)
    successMessage.value = 'Registration successful! Redirecting to login...'
    
    // Reset form
    Object.keys(form).forEach(key => form[key] = '')
    
    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>