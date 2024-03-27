<template>
  <table-box>
    <table-header-titles
      :titles="[
        ['Mortgage Term', SortBy.MortgageTerm],
        ['Monthly Payment', SortBy.MonthlyPayment],
        ['Interest Rate', SortBy.InterestRate],
        ['Total Amount', SortBy.TotalAmount],
        ['Total Over Loan Term', SortBy.TotalOverLoanTerm]
      ]"
      :get-loans="getLoans"
    />
    <tr
      v-for="(loan, index) in loans as Loan[]"
      :key="index"
      class="focus:outline-none h-16 border-t-2 border-t-gray-200 rounded hover:bg-gray-100"
    >
      <table-row :item="loan" />
    </tr>
  </table-box>
</template>

<script setup lang="ts">
import TableBox from '@/components/common/table/tableBox.vue'
import { Loan } from '@/domain/entities/loan'
import TableRow from '@/components/calculator/loanTableRow.vue'
import TableHeaderTitles from '@/components/common/table/tableHeaderTitles.vue'
import { SortBy } from '@/domain/enums/sortBy'

defineProps(['loans', 'getLoans'])
</script>
