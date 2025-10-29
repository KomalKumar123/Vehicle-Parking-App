<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">
          <i class="bi bi-shield-check me-2"></i>
          Admin Dashboard
        </h1>

        <ErrorAlert :message="errorMessage" @clear="errorMessage = ''" />

        <div class="row mb-4">
          <div class="col-md-3 mb-3">
            <div class="card bg-primary text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="card-title">Total Lots</h6>
                    <h3 class="mb-0">{{ summary.total_lots || 0 }}</h3>
                  </div>
                  <div class="align-self-center">
                    <i class="bi bi-building" style="font-size: 2rem;"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="card bg-info text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="card-title">Total Spots</h6>
                    <h3 class="mb-0">{{ summary.total_spots || 0 }}</h3>
                  </div>
                  <div class="align-self-center">
                    <i class="bi bi-p-square" style="font-size: 2rem;"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="card bg-warning text-dark">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="card-title">Occupied</h6>
                    <h3 class="mb-0">{{ summary.occupied_spots || 0 }}</h3>
                  </div>
                  <div class="align-self-center">
                    <i class="bi bi-car-front-fill" style="font-size: 2rem;"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="card bg-success text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="card-title">Available</h6>
                    <h3 class="mb-0">{{ summary.available_spots || 0 }}</h3>
                  </div>
                  <div class="align-self-center">
                    <i class="bi bi-check-circle" style="font-size: 2rem;"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <button
              class="btn btn-success"
              data-bs-toggle="modal"
              data-bs-target="#createLotModal"
            >
              <i class="bi bi-plus-circle me-2"></i>
              Create New Lot
            </button>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="bi bi-table me-2"></i>
                  Lot Occupancy Details
                </h5>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Lot Name</th>
                        <th>Address</th>
                        <th>Capacity</th>
                        <th>Occupied</th>
                        <th>Available</th>
                        <th>Price/Hour</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="lot in adminLots" :key="lot.id">
                        <td>{{ lot.name }}</td>
                        <td>{{ lot.address }}</td>
                        <td>{{ lot.capacity }}</td>
                        <td>
                          <span class="badge bg-warning">{{ lot.capacity - lot.available_spots }}</span>
                        </td>
                        <td>
                          <span class="badge bg-success">{{ lot.available_spots }}</span>
                        </td>
                        <td>₹{{ lot.price_per_hour }}</td>
                        <td>
                          <button
                            class="btn btn-sm btn-outline-primary me-2"
                            @click="editLot(lot)"
                            data-bs-toggle="modal"
                            data-bs-target="#editLotModal"
                          >
                            <i class="bi bi-pencil"></i>
                          </button>
                          <button
                            class="btn btn-sm btn-outline-danger"
                            @click="deleteLot(lot.id)"
                          >
                            <i class="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="bi bi-people me-2"></i>
                  Registered Users
                </h5>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-striped">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="user in users" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>
                          <span
                            class="badge"
                            :class="user.role === 'admin' ? 'bg-danger' : 'bg-primary'"
                          >
                            {{ user.role }}
                          </span>
                        </td>
                        <td>
                          <button
                            class="btn btn-sm btn-outline-info"
                            @click="viewUserHistory(user)"
                            data-bs-toggle="modal"
                            data-bs-target="#historyModal">
                            <i class="bi bi-clock-history"></i> History
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="bi bi-grid me-2"></i>
                  Real-time Parking Spots Status
                </h5>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Spot ID</th>
                        <th>Lot Name</th>
                        <th>Spot Number</th>
                        <th>Status</th>
                        <th>Occupant</th>
                        <th>Start Time</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="spot in spotsStatus" :key="spot.id">
                        <td>{{ spot.id }}</td>
                        <td>{{ spot.lot_name }}</td>
                        <td>{{ spot.spot_number }}</td>
                        <td>
                          <span
                            class="badge"
                            :class="spot.status === 'Occupied' ? 'bg-danger' : 'bg-success'"
                          >
                            {{ spot.status }}
                          </span>
                        </td>
                        <td>{{ spot.occupant_username || '-' }}</td>
                        <td>{{ spot.current_booking_info.park_in_time ? formatDateTime(spot.current_booking_info.park_in_time) : '-' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="createLotModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Parking Lot</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="createLot">
            <div class="modal-body">
              <div class="mb-3">
                <label for="createName" class="form-label">Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="createName"
                  v-model="createForm.name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="createAddress" class="form-label">Address</label>
                <textarea
                  class="form-control"
                  id="createAddress"
                  v-model="createForm.address"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="createPinCode" class="form-label">PIN Code</label>
                <input
                  type="text"
                  class="form-control"
                  id="createPinCode"
                  v-model="createForm.pin_code"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="createPrice" class="form-label">Price per Hour (₹)</label>
                <input
                  type="number"
                  class="form-control"
                  id="createPrice"
                  v-model="createForm.price_per_hour"
                  step="0.01"
                  min="0"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="createCapacity" class="form-label">Capacity</label>
                <input
                  type="number"
                  class="form-control"
                  id="createCapacity"
                  v-model="createForm.capacity"
                  min="1"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Cancel
              </button>
              <button type="submit" class="btn btn-success" :disabled="isCreating">
                <span v-if="isCreating" class="spinner-border spinner-border-sm me-2"></span>
                Create Lot
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editLotModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Parking Lot</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="updateLot">
            <div class="modal-body">
              <div class="mb-3">
                <label for="editName" class="form-label">Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editName"
                  v-model="editForm.name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="editAddress" class="form-label">Address</label>
                <textarea
                  class="form-control"
                  id="editAddress"
                  v-model="editForm.address"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="editPinCode" class="form-label">PIN Code</label>
                <input
                  type="text"
                  class="form-control"
                  id="editPinCode"
                  v-model="editForm.pin_code"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="editPrice" class="form-label">Price per Hour (₹)</label>
                <input
                  type="number"
                  class="form-control"
                  id="editPrice"
                  v-model="editForm.price_per_hour"
                  step="0.01"
                  min="0"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="editCapacity" class="form-label">Capacity</label>
                <input
                  type="number"
                  class="form-control"
                  id="editCapacity"
                  v-model="editForm.capacity"
                  min="1"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isUpdating">
                <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2"></span>
                Update Lot
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal fade" id="historyModal" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Booking History for: {{ selectedUsername }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <BookingHistory :key="selectedUserId" :userId="selectedUserId" />
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
import BookingHistory from '@/components/BookingHistory.vue'

const errorMessage = ref('')
const isCreating = ref(false)
const isUpdating = ref(false)
const selectedUserId = ref(null);
const selectedUsername = ref('');

const summary = reactive({
  total_lots: 0,
  total_spots: 0,
  occupied_spots: 0,
  available_spots: 0
})

const adminLots = ref([])
const users = ref([])
const spotsStatus = ref([])

const createForm = reactive({
  name: '',
  address: '',
  pin_code: '',
  price_per_hour: 0,
  capacity: 0
})

const editForm = reactive({
  id: null,
  name: '',
  address: '',
  pin_code: '',
  price_per_hour: 0,
  capacity: 0
})

const formatDateTime = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString()
}

const loadSummary = async () => {
  try {
    const response = await api.get('/admin/dashboard/summary')
    summary.total_lots = response.data.total_lots || 0
    summary.total_spots = response.data.total_spots || 0
    summary.occupied_spots = response.data.occupied_spots || 0
    summary.available_spots = response.data.available_spots || 0
  } catch (error) {
    errorMessage.value = 'Failed to load dashboard summary'
  }
}

const loadAdminLots = async () => {
  try {
    const response = await api.get('/admin/lots')
    adminLots.value = response.data
  } catch (error) {
    errorMessage.value = 'Failed to load lots'
  }
}

const loadUsers = async () => {
  try {
    const response = await api.get('/admin/users')
    users.value = response.data
  } catch (error) {
    errorMessage.value = 'Failed to load users'
  }
}

const loadSpotsStatus = async () => {
  try {
    const response = await api.get('/admin/spots/status');
    const spots = response.data;

    // Sort the array to show "Occupied" spots first
    spots.sort((a, b) => {
      if (a.status === 'Occupied' && b.status !== 'Occupied') {
        return -1; // a comes first
      }
      if (a.status !== 'Occupied' && b.status === 'Occupied') {
        return 1; // b comes first
      }
      // For spots with the same status, you could add secondary sort criteria here
      // For example, by lot_name, then by spot_number
      if (a.lot_name < b.lot_name) return -1;
      if (a.lot_name > b.lot_name) return 1;
      return a.spot_number - b.spot_number;
    });

    spotsStatus.value = spots;
  } catch (error) {
    errorMessage.value = 'Failed to load spots status';
  }
}

const createLot = async () => {
  isCreating.value = true
  try {
    await api.post('/admin/lots', createForm)

    // First, refresh all the data from the server
    await Promise.all([loadSummary(), loadAdminLots(), loadSpotsStatus()])

    // Then, reset the form
    Object.keys(createForm).forEach(key => {
      createForm[key] = typeof createForm[key] === 'number' ? 0 : ''
    })

    // Finally, hide the modal
    const modalElement = document.getElementById('createLotModal')
    const modal = bootstrap.Modal.getInstance(modalElement)
    if (modal) {
      modal.hide()
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Failed to create lot'
  } finally {
    isCreating.value = false
  }
}

const editLot = (lot) => {
  editForm.id = lot.id
  editForm.name = lot.name
  editForm.address = lot.address
  editForm.pin_code = lot.pin_code
  editForm.price_per_hour = lot.price_per_hour
  editForm.capacity = lot.capacity
}

const updateLot = async () => {
  isUpdating.value = true
  try {
    const { id, ...updateData } = editForm
    await api.put(`/admin/lots/${id}`, updateData)

    // First, refresh all the data from the server
    await Promise.all([loadSummary(), loadAdminLots(), loadSpotsStatus()])

    // Finally, hide the modal
    const modalElement = document.getElementById('editLotModal')
    const modal = bootstrap.Modal.getInstance(modalElement)
    if (modal) {
        modal.hide()
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Failed to update lot'
  } finally {
    isUpdating.value = false
  }
}

const deleteLot = async (lotId) => {
  if (!confirm('Are you sure you want to delete this parking lot? This action cannot be undone.')) {
    return
  }

  try {
    await api.delete(`/admin/lots/${lotId}`)
    await Promise.all([loadSummary(), loadAdminLots(), loadSpotsStatus()])
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Failed to delete lot'
  }
}

const viewUserHistory = (user) => {
  selectedUserId.value = user.id;
  selectedUsername.value = user.username;
};

onMounted(() => {
  loadSummary()
  loadAdminLots()
  loadUsers()
  loadSpotsStatus()
})
</script>