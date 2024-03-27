<template>
  <div class="flex justify-start">
    <rates-form v-model="ratesData" @calculate="calculate" style="align-self: flex-start" />
    <loans-table :loans="loans" :get-loans="getLoans" />
  </div>
</template>
<script lang="ts" setup>
import loansTable from '@/components/calculator/loansTable.vue'
import ratesForm from '@/components/calculator/ratesForm.vue'
import { RatesInput } from '@/domain/entities/ratesInput'
import { onMounted, ref } from 'vue'

const ratesData = ref<RatesInput>({})

defineProps(['loans', 'getLoans'])
const emit = defineEmits<{
  generateRates: [data: any]
}>()

const calculate = () => {
  emit('generateRates', ratesData.value)
  clearRatesForm()
}

const clearRatesForm = () => {
  ratesData.value = {
    purchasePrice: undefined,
    interestRate: undefined,
    dollarDownPayment: undefined,
    percentageDownPayment: undefined,
    mortgageTerm: undefined
  }
}

onMounted(clearRatesForm)
</script>
