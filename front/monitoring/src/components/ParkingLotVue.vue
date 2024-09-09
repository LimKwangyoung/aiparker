<template>
  <v-container class="d-flex flex-column">
    <div class="title mb-2">주차 현황</div>
    <div class="box d-flex flex-column px-2 elevation-1">
      <div v-for="(row, rowIndex) in region" :key="rowIndex" class='d-flex flex-grow-1 my-4'>
        <div v-for="(col, colIndex) in row" :key="colIndex"
          :class="[region[rowIndex][colIndex], store.occupancyInfo[region[rowIndex][colIndex]] != null ? 'occupied' : '']">
          <div v-if="store.occupancyInfo[region[rowIndex][colIndex]] != null" class="number">
            <div>{{ store.occupancyInfo[region[rowIndex][colIndex]].slice(0, -4) }}</div>
            <div>{{ store.occupancyInfo[region[rowIndex][colIndex]].slice(-4) }}</div>
          </div>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script setup>
import { useMonitorStore } from '@/stores/monitor.js'

const region = [
  ['S1', 'S2', 'S3', 'S4', 'P', 'E1', 'E2'],
  ['P', 'P', 'A1', 'A2', 'A3', 'P', 'P'],
  ['P', 'P', 'B1', 'B2', 'B3', 'P', 'P'],
  ['P', 'P', 'C1', 'C2', 'C3', 'P', 'P'],
]

const coord = {
  'S1': (0, 0), 'S2': (0, 1), 'S3': (0, 2), 'S4': (0, 3),
  'E1': (0, 5), 'S2': (0, 6),
  'A1': (1, 2), 'A2': (1, 3), 'A3': (1, 4),
  'B1': (2, 2), 'B2': (2, 3), 'B3': (2, 4),
  'C1': (3, 2), 'C2': (3, 3), 'C3': (3, 4),
}

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
  height: 100%;

  border: 2px solid black;
  border-radius: 8px;
  background-color: whitesmoke;
}

.S1,
.S2,
.S3,
.S4,
.E1,
.E2,
.A1,
.A2,
.A3,
.B1,
.B2,
.B3,
.C1,
.C2,
.C3,
.P {
  flex-grow: 1;
  margin-left: 3px;
  margin-right: 3px;
}

.S1,
.S2,
.S3,
.S4,
.E1,
.E2,
.A1,
.A2,
.A3,
.B1,
.B2,
.B3,
.C1,
.C2,
.C3 {
  border-radius: 4px;
  background-color: lightgray;
}

.occupied {
  position: relative;

  background-color: #FFAFAF;
}

.number {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>