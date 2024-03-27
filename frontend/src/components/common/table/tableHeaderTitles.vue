<template>
  <td
    v-for="(title, index) in titles"
    :key="index"
    class="focus:outline-none h-10 pl-5 text-gray-600"
  >
    <div class="flex flex-row font-medium">
      {{ title[0] }}
      <div class="flex flex-col mx-4">
        <arrow-up class="mb-0.5" @click="getLoans(title[1], OrderBy.Ascending)" />
        <arrow-down @click="getLoans(title[1], OrderBy.Descending)" />
      </div>
    </div>
  </td>
</template>

<script lang="ts" setup>
import ArrowUp from '@/components/common/icon/arrowUp.vue'
import ArrowDown from '@/components/common/icon/arrowDown.vue'
import { OrderBy } from '@/domain/enums/orderBy'

defineProps(['titles', 'getLoans'])
</script>
