<template>
  <div class="text-center pt-2">
    <button
      class="w-full text-white py-1 rounded-lg cursor-pointer transition-transform duration-200 transform hover:scale-105 btn active:scale-90"
      style="background: #2491eb"
      type="submit"
      @click="$emit('click')"
    >
      <slot />
    </button>
  </div>
</template>

<script setup lang="ts">
defineEmits(['click'])
</script>

<style>
.btn {
  background: #2491eb;
}
</style>
