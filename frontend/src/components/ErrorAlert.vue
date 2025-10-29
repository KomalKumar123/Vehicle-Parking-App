<template>
  <div v-if="message" class="alert alert-danger alert-dismissible fade show mb-4" role="alert">
    <i class="bi bi-exclamation-triangle-fill me-2"></i>
    {{ message }}
    <button type="button" class="btn-close" @click="$emit('clear')" aria-label="Close"></button>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: ''
  }
})

defineEmits(['clear'])
</script>