<template>
  <div class="py-8 mx-auto">
    <div class="title text-indigo-900">
      {{ title }}
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps(['title'])
</script>

<style>
.title {
  font-size: 3.25rem;
  font-weight: 370;
}
</style>
