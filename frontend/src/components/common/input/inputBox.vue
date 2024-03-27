<template>
  <div class="flex flex-col items-start mt-3 mb-6">
    <label
      v-if="label"
      :for="name"
      class="block mb-2 mx-1 text-md text-indigo-900 relative font-medium"
    >
      {{ label }}&nbsp;
      <span v-if="required" class="font-bold absolute bottom-1.5">*</span>
    </label>
    <Field
      class="flex w-full border rounded-lg py-2 px-3 resize-none text-gray-600 text-md"
      :placeholder="placeholder"
      v-bind="$attrs"
      :type="type"
      :name="name"
      :id="name"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <ErrorMessage :name="name" class="text-red-500 text-sm" />
  </div>
</template>

<script setup lang="ts">
import { ErrorMessage, Field } from 'vee-validate'
defineProps(['label', 'type', 'placeholder', 'modelValue', 'name', 'required'])
</script>
