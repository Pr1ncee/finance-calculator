<template>
  <table-cell>
    {{ item.mortgageTerm }}
  </table-cell>
  <table-cell>
    {{ item.monthlyPayment }}
  </table-cell>
  <table-cell>
    {{ item.interestRate }}
  </table-cell>
  <table-cell>
    {{ item.totalAmount }}
  </table-cell>
  <table-cell>
    {{ item.totalOverLoanTerm }}
  </table-cell>
</template>
<script lang="ts" setup>
import TableCell from '@/components/common/table/tableCell.vue'
import { Loan } from '@/domain/entities/loan'

defineProps<{
  item: Loan
}>()
</script>
