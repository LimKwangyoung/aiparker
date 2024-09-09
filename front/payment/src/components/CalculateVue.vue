<template>
  <v-container class="d-flex flex-column justify-end">
    <div class="box mb-10 d-flex flex-column justify-center align-center elevation-1">
      <div class="title pb-5">남은 주차 구역 수</div>
      <div class="content" style="color: green;">{{ 15 - store.occupancyNumber }}</div>
    </div>
    <div class="box mb-10 d-flex flex-column justify-center align-center elevation-1">
      <div class="title pb-5">주차 차량 수</div>
      <div class="content" style="color: red;">{{ store.occupancyNumber }}</div>
    </div>
    <div class="box d-flex flex-column justify-center align-center elevation-1">
      <div class="title pb-5">정산 현황</div>
      <div class="content">{{ store.totalPrice }} 원</div>
    </div>
  </v-container>
</template>

<script setup>
import { useMonitorStore } from '@/stores/monitor.js'

const store = useMonitorStore()
</script>

<style scoped>
.v-container {
  width: 70%;
  height: 500px;

  padding-top: 40px !important;
}

.box {
  flex-grow: 1;

  border: 2px solid black;
  border-radius: 8px;
  background-color: whitesmoke;
}

.title {
  font-size: 1.5rem;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}

.content {
  font-size: 2rem;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}
</style>