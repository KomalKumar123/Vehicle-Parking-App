<template>
  <div class="col-md-4 mb-4">
    <div class="card h-100">
      <div class="card-body">
        <h5 class="card-title">{{ lot.name }}</h5>
        <p class="card-text text-muted">
          <i class="bi bi-geo-alt-fill me-1"></i>
          {{ lot.address }}
        </p>
        <div class="d-flex justify-content-between mb-2">
          <span class="badge bg-primary">Capacity: {{ lot.capacity }}</span>
          <span class="badge bg-success">Available: {{ lot.available_spots }}</span>
        </div>
        <p class="card-text">₹{{ lot.price_per_hour }} / hour</p>
      </div>
      <div class="card-footer bg-transparent">
        <button
          class="btn btn-primary w-100"
          @click="bookSpot"
          :disabled="isBooking || lot.available_spots === 0"
        >
          <span v-if="isBooking" class="spinner-border spinner-border-sm me-2"></span>
          {{ lot.available_spots === 0 ? 'No Spots Available' : 'Book Spot' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/store/auth'

const props = defineProps({
  lot: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['booked', 'error'])

const isBooking = ref(false)
const authStore = useAuthStore()

const bookSpot = async () => {
  isBooking.value = true
  try {
    await api.post(`/api/book/${props.lot.id}`)
    emit('booked')
  } catch (error) {
    emit('error', error.response?.data?.message || 'Failed to book spot')
  } finally {
    isBooking.value = false
  }
}
</script>