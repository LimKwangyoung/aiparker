<template>
  <v-container class="pt-15 pb-5 d-flex flex-column">
    <v-row class="pt-10">
      <v-col cols="4">
        <v-card elevation="5" rounded="xl">
          <v-card-item>
            <!-- <v-img src="/images/empty.png" class="mx-auto py-5"></v-img> -->
            <!-- <ImageVue :img-src="store.carInfo['s3']" class="mx-auto py-10" /> -->
            <v-img :src="store.carInfo['s3']" class="mx-auto py-10"></v-img>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="8">
        <v-table class="ml-10">
          <tr>
            <td class="table-header">차량 번호</td>
            <td class="table-content">{{ store.carInfo['licensePlate'].slice(0, -4) }} {{
              store.carInfo['licensePlate'].slice(-4) }}</td>
          </tr>
          <tr>
            <td class="table-header">입차 시각</td>
            <!-- <td class="table-content">{{ store.carInfo['entryTime'].slice(-8) }}</td> -->
            <td class="table-content">{{ entryTime.slice(-8) }}</td>
          </tr>
          <tr>
            <td class="table-header">주차 시간</td>
            <td class="table-content">
              <span v-if="Math.floor(parkingTime / 3600).toString().padStart(2, '0') !== '00'">
                {{ Math.floor(parkingTime / 3600) }}시간
              </span>
              <span
                v-if="(Math.floor(parkingTime / 60) - Math.floor(parkingTime / 3600) * 60).toString().padStart(2, '0') !== '00'">
                {{ (Math.floor(parkingTime / 60) - Math.floor(parkingTime / 3600) * 60) }}분
              </span>
            </td>
          </tr>
          <tr>
            <td class="table-header">주차 구역</td>
            <td class="table-content">{{ store.carInfo['parkingSpot']['code'] }}</td>
          </tr>
          <tr>
            <td class="table-last-header">결제 금액</td>
            <td class="table-last-content">{{ store.fee }} 원</td>
          </tr>
        </v-table>
      </v-col>
    </v-row>
    <v-row class="bottom-fixed">
      <v-col class="d-flex align-center" cols=4>
        <v-btn class="btn-sub py-3" rounded="xl" @click="goMain">
          <v-icon icon="mdi-home"></v-icon>
        </v-btn>
      </v-col>
      <v-col class="d-flex align-center justify-space-evenly" cols="8">
        <v-btn class="btn-sub py-3" rounded="xl" @click="goBack">이전으로</v-btn>
        <v-btn class="btn-sub py-3" rounded="xl" @click="goPay">정산하기</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useParkingStore } from '@/stores/parking.js'

import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)

// import ImageVue from '@/components/ImageVue.vue'

const router = useRouter()
const store = useParkingStore()

const parkingTime = ref(null)
const entryTime = ref(dayjs.utc(store.carInfo['entryTime']).tz('Asia/Seoul').format('YYYY-MM-DD HH:mm:ss'))

onMounted(() => {
  entryTime.value = dayjs.utc(store.carInfo['entryTime']).tz('Asia/Seoul').format('YYYY-MM-DD HH:mm:ss')

  const date = new Date()
  const endYear = date.getFullYear()
  const endMonth = date.getMonth() + 1
  const endDate = date.getDate()
  const endHour = date.getHours()
  const endMinute = date.getMinutes()
  const endSecond = date.getSeconds()

  store.exitTime = `${endYear}-${endMonth.toString().padStart(2, '0')}-${endDate.toString().padStart(2, '0')}T${endHour.toString().padStart(2, '0')}:${endMinute.toString().padStart(2, '0')}:${endSecond.toString().padStart(2, '0')}`

  const startHour = Number(entryTime.value.slice(-8).slice(0, 2))
  const startMinute = Number(entryTime.value.slice(-8).slice(3, 5))
  const startSecond = Number(entryTime.value.slice(-8).slice(6, 8))

  const startTime = startHour * 60 * 60 + startMinute * 60 + startSecond
  const endTime = endHour * 60 * 60 + endMinute * 60 + endSecond

  parkingTime.value = endTime - startTime

  // 10분에 500원
  store.fee = Math.floor(parkingTime.value / 60 / 10) * 500
})

const goPay = function () {
  router.push({ name: 'pay' })
}

const goMain = function () {
  router.push({ name: 'main' })
}

const goBack = function () {
  router.push({ name: 'select' })
}
</script>

<style scoped>
.v-container {
  max-width: none;
}

/* .v-col {
  padding: 0;
} */

.v-card {
  background-color: whitesmoke;
}

/* .v-img {
  width: 90%;
} */

.v-table {
  border: 8px solid #379777;
  border-radius: 8px;
  background-color: #FFFCEE;

  text-align: center;
}

td {
  padding-top: 12px;
  padding-bottom: 12px;
}

.last-row {
  border: none;
}

.table-header,
.table-last-header {
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1.05;
  letter-spacing: normal;

  width: 40%;
  border-right: 6px solid #379777;
}

.table-content,
.table-last-content {
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1.05;
  letter-spacing: normal;
}

.table-header,
.table-content {
  border-bottom: 6px solid #379777;
}

.bottom-fixed {
  min-height: 120px;
  max-height: 120px;
}

.btn-sub {
  /* width: auto !important; */
  height: auto !important;

  font-size: 3rem;
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.0083333333em;
  color: white;

  background-color: #379777;
}
</style>