<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">
          <i class="bi bi-speedometer2 me-2"></i>
          User Dashboard
        </h1>

        <ErrorAlert :message="errorMessage" @clear="errorMessage = ''" />

        <div class="row mb-4">
          <div class="col-md-6 mb-3">
            <div class="card bg-primary text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h5 class="card-title">Total Bookings</h5>
                    <h2 class="mb-0">{{ summary.total_bookings || 0 }}</h2>
                  </div>
                  <div class="align-self-center">
                    <i class="bi bi-calendar-check" style="font-size: 2rem;"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6 mb-3">
            <div class="card bg-success text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h5 class="card-title">Total Spent</h5>
                    <h2 class="mb-0">₹{{ summary.total_spent?.toFixed(2) || '0.00' }}</h2>
                  </div>
                  <div class="align-self-center">
                    <i class="bi bi-currency-rupee" style="font-size: 2rem;"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeBooking" class="row mb-4">
          <div class="col-12">
            <div class="card border-warning">
              <div class="card-header bg-warning text-dark">
                <h5 class="mb-0">
                  <i class="bi bi-car-front-fill me-2"></i>
                  Active Booking
                </h5>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-8">
                    <h6>{{ activeBooking.lot_name }}</h6>
                    <p class="text-muted mb-1">
                      <i class="bi bi-geo-alt-fill me-1"></i>
                      {{ activeBooking.lot_address }}
                    </p>
                    <p class="mb-1">
                      <strong>Spot:</strong> {{ activeBooking.spot_number }}
                    </p>
                    <p class="mb-1">
                      <strong>Start Time:</strong> {{ formatDateTime(activeBooking.start_time) }}
                    </p>
                  </div>
                  <div class="col-md-4 text-end align-self-center">
                    <button
                      class="btn btn-danger"
                      @click="releaseSpot"
                      :disabled="isReleasing"
                    >
                      <span v-if="isReleasing" class="spinner-border spinner-border-sm me-2"></span>
                      Release Spot
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <button
              class="btn btn-info me-2"
              @click="exportHistory"
              :disabled="isExporting"
            >
              <span v-if="isExporting" class="spinner-border spinner-border-sm me-2"></span>
              <i class="bi bi-download me-2"></i>
              Export My History (CSV)
            </button>
            <button
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#userHistoryModal">
              <i class="bi bi-clock-history me-2"></i>
              View My Booking History
            </button>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <h3 class="mb-3">
              <i class="bi bi-p-square me-2"></i>
              Available Parking Lots
            </h3>

            <div v-if="isLoadingLots" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div v-else-if="lots.length === 0" class="alert alert-info">
              <i class="bi bi-info-circle-fill me-2"></i>
              No parking lots available at the moment.
            </div>

            <div v-else class="row">
              <LotCard
                v-for="lot in lots"
                :key="lot.id"
                :lot="lot"
                @booked="handleBookingSuccess"
                @error="handleBookingError"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="userHistoryModal" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">My Booking History</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <BookingHistory />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/services/api'
import ErrorAlert from '@/components/ErrorAlert.vue'
import LotCard from '@/components/LotCard.vue'
import BookingHistory from '@/components/BookingHistory.vue'

const errorMessage = ref('')
const isLoadingLots = ref(false)
const isReleasing = ref(false)
const isExporting = ref(false)

const summary = reactive({
  total_bookings: 0,
  total_spent: 0
})

const activeBooking = ref(null)
const lots = ref([])

const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString()
}

const loadSummary = async () => {
  try {
    const response = await api.get('/api/dashboard/summary')
    Object.assign(summary, response.data)
  } catch (error) {
    console.error('Failed to load summary:', error)
  }
}

const loadActiveBooking = async () => {
  try {
    const response = await api.get('/api/booking/active')
    activeBooking.value = response.data
  } catch (error) {
    if (error.response?.status !== 404) {
      errorMessage.value = 'Failed to check for an active booking.'
    } else {
        activeBooking.value = null;
    }
  }
}

const loadLots = async () => {
  isLoadingLots.value = true
  try {
    const response = await api.get('/api/lots')
    lots.value = response.data
  } catch (error) {
    errorMessage.value = 'Failed to load parking lots'
  } finally {
    isLoadingLots.value = false
  }
}

const releaseSpot = async () => {
  isReleasing.value = true
  try {
    await api.post('/api/booking/release')
    activeBooking.value = null
    // Refresh all data to reflect the changes
    await Promise.all([loadSummary(), loadLots()]);
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Failed to release spot'
  } finally {
    isReleasing.value = false
  }
}

const exportHistory = async () => {
  isExporting.value = true
  try {
    await api.post('/api/export/csv')
    // A more robust solution might use a toast library
    alert("CSV export initiated! You'll receive an email when it's ready.");
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Failed to export history'
  } finally {
    isExporting.value = false
  }
}

const handleBookingSuccess = () => {
  // Refresh all relevant data after a successful booking
  loadActiveBooking()
  loadSummary()
  loadLots()
}

const handleBookingError = (error) => {
  errorMessage.value = error
}

onMounted(() => {
  loadSummary()
  loadActiveBooking()
  loadLots()
})
</script>