<template>
  <div class="modal fade" id="createLotModal" tabindex="-1" aria-labelledby="createLotModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="createLotModalLabel">Create New Parking Lot</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <ErrorAlert :message="errorMessage" @dismiss="errorMessage = ''" />
          <form @submit.prevent="createLot">
            <div class="mb-3">
              <label for="name" class="form-label">Lot Name</label>
              <input type="text" class="form-control" v-model="form.name" required>
            </div>
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <input type="text" class="form-control" v-model="form.address" required>
            </div>
            <div class="mb-3">
              <label for="pin_code" class="form-label">Pin Code</label>
              <input type="text" class="form-control" v-model="form.pin_code" required>
            </div>
            <div class="mb-3">
              <label for="price" class="form-label">Price per Hour</label>
              <input type="number" step="0.01" class="form-control" v-model.number="form.price_per_hour" required>
            </div>
            <div class="mb-3">
              <label for="capacity" class="form-label">Capacity</label>
              <input type="number" class="form-control" v-model.number="form.capacity" required>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">Create Lot</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '@/services/api';
import ErrorAlert from '@/components/ErrorAlert.vue';
import { Modal } from 'bootstrap';

const emit = defineEmits(['lot-created']);
const form = reactive({
  name: '',
  address: '',
  pin_code: '',
  price_per_hour: 0,
  capacity: 0
});
const errorMessage = ref('');
const loading = ref(false);

const createLot = async () => {
    loading.value = true;
    errorMessage.value = '';
    try {
        const response = await apiClient.post('/admin/lots', form);
        emit('lot-created', response.data.msg);
        const modal = Modal.getInstance(document.getElementById('createLotModal'));
        modal.hide();
        // Reset form
        Object.assign(form, { name: '', address: '', pin_code: '', price_per_hour: 0, capacity: 0 });
    } catch (error) {
        errorMessage.value = error.response?.data?.msg || 'Failed to create lot.';
    } finally {
        loading.value = false;
    }
};
</script>