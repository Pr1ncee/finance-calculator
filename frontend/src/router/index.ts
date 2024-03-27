import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import LoanCalculator from '@/views/LoanCalculator.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Calculator',
    component: LoanCalculator
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router
