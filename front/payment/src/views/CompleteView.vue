<template>
  <v-container class="pt-15 pb-15 d-flex flex-column justify-space-evenly">
    <div class="text-center">
      <p class="mb-10">
        정산이 완료되었습니다.
      </p>
      <p>
        {{ store.carInfo['parkingSpot']['code'] }} 구역에 주차되어 있습니다.
      </p>
    </div>
    <div class="d-flex justify-space-evenly">
      <v-btn @click="goMain" class="px-10 py-5" rounded="xl">처음으로</v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useParkingStore } from '@/stores/parking.js'

import axios from 'axios'

const router = useRouter()
const store = useParkingStore()

const data = {
  'id': store.carInfo['id'],
  'exitTime': `${store.exitTime.slice(0, 11)}${(Number(store.exitTime.slice(-8, -6)) - 9).toString().padStart(2, '0')}${store.exitTime.slice(-6)}`,
  'fee': store.fee
}

// console.log(`${store.exitTime.slice(0, 11)}${(Number(store.exitTime.slice(-8, -6)) - 9).toString().padStart(2, '0')}${store.exitTime.slice(-6)}`)


onMounted(() => {
  axios.post('https://i11a104.p.ssafy.io/api/payment/complete', data)
    .then(res => console.log(res))
    .catch(err => {
      console.error('Error:', err.response)
    })
})

const goMain = function () {
  router.push({ name: 'main' })
}
</script>

<style scoped>
.v-container {
  max-width: none;
}

div {
  font-size: 4rem;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.015625em
}

.v-btn {
  height: auto !important;

  font-size: 3rem;
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.0083333333em;
  color: white;

  background-color: #379777;
}
</style>
