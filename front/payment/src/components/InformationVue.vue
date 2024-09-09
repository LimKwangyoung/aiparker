<template>
  <v-container>
    <div class="title mb-2">입차 정보</div>
    <div class="box mb-5 px-3 py-2 elevation-1">
      <div v-for="info in store.entrySortInfo.slice(-6)" :key="info.id" class="my-1">
        <span v-if="info['entryTime'] !== null" class="mr-3" style="color: green;">{{ info['entryTime'].slice(0, 10) }}
          {{ info['entryTime'].slice(11) }}</span>
        <span v-if="info['entryTime'] !== null">{{ info['licensePlate'] }}</span>
      </div>
    </div>
    <div class="title mb-2">출차 정보</div>
    <div class="box mb-5 px-3 py-2 elevation-1">
      <div v-for="info in store.exitSortArray.slice(-6)" :key="info.id" class="my-1">
        <span v-if="info['exitTime'] !== null" class="mr-3" style="color: red;">{{ info['exitTime'].slice(0, 10) }} {{
          info['exitTime'].slice(11) }}</span>
        <span v-if="info['exitTime'] !== null">{{ info['licensePlate'] }}</span>
      </div>
    </div>
  </v-container>
</template>

<script setup>
import { useMonitorStore } from '@/stores/monitor.js'

const store = useMonitorStore()
</script>

<style scoped>
.v-container {
  height: 500px;
}

.title {
  font-size: 2rem;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}

.box {
  height: 200px;

  border: 2px solid black;
  border-radius: 8px;
  background-color: whitesmoke;
}

span {
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.6;
  letter-spacing: 0.0125em;
}
</style>