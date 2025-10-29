<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body p-4">
            <div class="text-center mb-4">
              <i class="bi bi-car-front-fill text-primary" style="font-size: 3rem;"></i>
              <h2 class="mt-2">Login</h2>
              <p class="text-muted">Welcome back to Vehicle Parking System</p>
            </div>

            <ErrorAlert :message="errorMessage" @clear="errorMessage = ''" />

            <form @submit.prevent="handleLogin">
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
                />
              </div>
              
              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                Login
              </button>
            </form>

            <div class="text-center mt-3">
              <p class="mb-0">
                Don't have an account?
                <router-link to="/register" class="text-decoration-none">Register here</router-link>
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

const form = reactive({
  email: '',
  password: ''
})

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    await authStore.login(form)
    
    // Redirect based on role
    if (authStore.role === 'admin') {
      router.push('/admin/dashboard')
    } else {
      router.push('/dashboard')
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>