<template>
  <Form
    :validation-schema="schema"
    @submit="generate"
    class="p-12 text-lg mr-12 bg-white rounded-xl"
    style="width: 28%"
    :key="data"
  >
    <input-box
      v-model="data.purchasePrice"
      :required="true"
      label="Purchase Price"
      type="number"
      placeholder="E.g. $ 100,000.000"
      name="purchasePrice"
    />
    <input-box
      v-model="data.interestRate"
      :required="true"
      label="Interest Rate"
      type="number"
      placeholder="E.g. 20 %"
      name="interestRate"
    />
    <input-box
      v-model="data.dollarDownPayment"
      label="Down Payment in $"
      type="number"
      placeholder="E.g. $ 15,000.000"
      name="downPaymentDollars"
    />
    <input-box
      v-model="data.percentageDownPayment"
      label="Down Payment in %"
      type="number"
      placeholder="E.g. 20 %"
      name="downPaymentPercentage"
    />
    <input-box
      v-model="data.mortgageTerm"
      :required="true"
      label="Mortgage Term"
      type="number"
      placeholder="E.g. 90 months"
      name="mortgageTerm"
    />
    <submit-button> Generate Rates </submit-button>
  </Form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SubmitButton from '@/components/common/button/submitButton.vue'
import InputBox from '@/components/common/input/inputBox.vue'
import { RatesInput } from '@/domain/entities/ratesInput'
import { Form } from 'vee-validate'
import * as yup from 'yup'

const props = defineProps<{
  modelValue: any
}>()
const emit = defineEmits(['update:modelValue', 'calculate'])
const data = ref<RatesInput>(props.modelValue)

const schema = yup.object().shape({
  purchasePrice: yup.number().required().min(0),
  interestRate: yup.number().required().min(0),
  downPaymentDollars: yup
    .number()
    .nullable()
    .transform((value, originalValue) => {
      return transformEmptyToUndefined(originalValue)
    })
    .min(0),
  downPaymentPercentage: yup
    .number()
    .nullable()
    .min(0)
    .max(100)
    .transform((value, originalValue) => {
      return transformEmptyToUndefined(originalValue)
    })
    .test(
      'Not both empty',
      'Either downPaymentDollars or downPaymentPercentage must have a value',
      function (value) {
        const downPaymentDollars = this.parent.downPaymentDollars
        return value !== undefined || downPaymentDollars !== undefined
      }
    ),
  mortgageTerm: yup.number().required().min(0)
})

const generate = () => {
  emit('update:modelValue', data.value)
  emit('calculate')
  data.value = props.modelValue
}

const transformEmptyToUndefined = (value: number | string) => {
  const stringValue = String(value || '')
  return stringValue.trim() === '' ? undefined : value
}
</script>
