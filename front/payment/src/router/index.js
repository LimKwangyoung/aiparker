import { createRouter, createWebHistory } from 'vue-router'

import MonitoringMainView from '@/views/MonitoringMainView.vue'

import PaymentMainView from '@/views/PaymentMainView.vue'
import InputView from '@/views/InputView.vue'
import SelectView from '@/views/SelectView.vue'
import DetailView from '@/views/DetailView.vue'
import PayView from '@/views/PayView.vue'
import CompleteView from '@/views/CompleteView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/monitoring',
      name: 'monitoring',
      component: MonitoringMainView
    },
    {
      path: '/payment',
      name: 'main',
      component: PaymentMainView
    },
    {
      path: '/payment/input',
      name: 'input',
      component: InputView
    },
    {
      path: '/payment/select',
      name: 'select',
      component: SelectView
    },
    {
      path: '/payment/detail',
      name: 'detail',
      component: DetailView
    },
    {
      path: '/payment/pay',
      name: 'pay',
      component: PayView
    },
    {
      path: '/payment/complete',
      name: 'complete',
      component: CompleteView
    },
  ]
})

export default router
