<template>
  <div>
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading history...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="bookings.length === 0" class="alert alert-info">
      <i class="bi bi-info-circle-fill me-2"></i>
      No booking history found.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Booking ID</th>
            <th>Lot Name</th>
            <th>Spot</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td>{{ booking.id }}</td>
            <td>{{ booking.lot_name }}</td>
            <td>{{ booking.spot_number }}</td>
            <td>{{ formatDateTime(booking.start_time) }}</td>
            <td>{{ formatDateTime(booking.end_time) }}</td>
            <td>₹{{ booking.cost?.toFixed(2) || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '@/services/api';

const props = defineProps({
  // The Admin dashboard will pass a userId.
  // The User dashboard will not, so it will be null.
  userId: {
    type: [Number, String],
    default: null
  }
});

const bookings = ref([]);
const isLoading = ref(false);
const error = ref('');

const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
};

const fetchHistory = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    let response;
    if (props.userId) {
      // Admin path: fetch history for a specific user
      response = await api.get(`/admin/bookings?user_id=${props.userId}`); //
    } else {
      // User path: fetch their own history
      response = await api.get('/api/history'); //
    }
    bookings.value = response.data;
  } catch (err) {
    error.value = 'Failed to load booking history.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

// Fetch data when the component is first created
onMounted(fetchHistory);

// And re-fetch if the userId prop ever changes (for the admin view)
watch(() => props.userId, fetchHistory);
</script>