<template>
  <div class="w-full px-24 md:px-28 xl:px-32 py-6 md:py-10 xl:py-14">
    <page-heading title="Loan Payment Calculator" />
    <calculator :loans="loans" :get-loans="getLoans" @generate-rates="generateRates" />
  </div>
</template>

<script setup lang="ts">
import calculator from '@/components/calculator/loanCalculator.vue'
import PageHeading from '@/components/common/other/pageHeading.vue'
import FetchHttpClient from '@/api/FetchHttpClient'
import FinanceCalculatorApi from '@/api/FinanceCalculatorApi'
import { onMounted, ref } from 'vue'
import { Loan } from '@/domain/entities/loan'
import { SortBy } from '@/domain/enums/sortBy'
import { OrderBy } from '@/domain/enums/orderBy'

const httpClient = new FetchHttpClient()
const financeCalculatorApi = new FinanceCalculatorApi(httpClient)
const loans = ref<Loan[]>([])

const generateRates = async (data: any) => {
  try {
    await financeCalculatorApi.generateRates(data)
    await getLoans()
  } catch (error) {
    console.error('Something went wrong:', error)
  }
}

const getLoans = async (sortBy?: SortBy, orderBy?: OrderBy) => {
  try {
    loans.value = await financeCalculatorApi.getLoans(sortBy, orderBy)
  } catch (error) {
    console.error('Something went wrong:', error)
  }
}

onMounted(getLoans)
</script>
<style>
body {
  background: #f4f4f4;
}
</style>
