<template>
  <v-container class="pt-15 pb-5 d-flex flex-column">
    <v-row>
      <v-col class="d-flex justify-space-between align-center" cols="7">
        <div class="number-box d-inline-block rounded-lg">{{ number1 }}</div>
        <div class="number-box d-inline-block rounded-lg">{{ number2 }}</div>
        <div class="number-box d-inline-block rounded-lg">{{ number3 }}</div>
        <div class="number-box d-inline-block rounded-lg">{{ number4 }}</div>
      </v-col>
      <v-col class="pl-1" cols="5">
        <v-container>
          <v-row class="justify-space-evenly pb-3">
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(1)">1</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(2)">2</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(3)">3</v-btn>
          </v-row>
          <v-row class="justify-space-evenly pb-3">
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(4)">4</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(5)">5</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(6)">6</v-btn>
          </v-row>
          <v-row class="justify-space-evenly pb-3">
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(7)">7</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(8)">8</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(9)">9</v-btn>
          </v-row>
          <v-row class="justify-space-evenly">
            <v-btn class="btn-main btn-clear" rounded="xl" @click="clearNumber">C</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="inputNumber(0)">0</v-btn>
            <v-btn class="btn-main btn-number" rounded="xl" @click="deleteNumber">←</v-btn>
          </v-row>
        </v-container>
      </v-col>
    </v-row>
    <v-row class="bottom-fixed">
      <v-col class="d-flex align-center" cols="7">
        <v-btn class="btn-sub py-3" rounded="xl" @click="goMain">
          <v-icon icon="mdi-home"></v-icon>
        </v-btn>
      </v-col>
      <v-col class="d-flex justify-center align-center pl-1" cols="5">
        <v-btn class="btn-sub px-10 py-3" rounded="xl" @click="goSelect">차량 조회하기</v-btn>
      </v-col>
    </v-row>

    <v-dialog v-model="query1">
      <v-card prepend-icon="mdi-alert" class="pa-5" rounded="lg">
        <template v-slot:title>
          <span>차량 번호를 입력해주세요</span>
        </template>
        <template v-slot:actions>
          <v-btn @click="query1 = false">확인</v-btn>
        </template>
      </v-card>
    </v-dialog>

    <v-dialog v-model="query2">
      <v-card prepend-icon="mdi-alert" class="pa-5" rounded="lg">
        <template v-slot:title>
          <span>조회된 차량 번호가 없습니다.</span>
        </template>
        <template v-slot:actions>
          <v-btn @click="query2 = false">확인</v-btn>
        </template>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useParkingStore } from '@/stores/parking.js'

const number1 = ref(null)
const number2 = ref(null)
const number3 = ref(null)
const number4 = ref(null)

const query1 = ref(false)
const query2 = ref(false)

const router = useRouter()
const store = useParkingStore()

const goMain = function () {
  router.push({ name: 'main' })
}

const inputNumber = function (number) {
  if (number4.value != null) {
    return
  }

  if (number1.value == null) {
    number1.value = number
  } else if (number2.value == null) {
    number2.value = number
  } else if (number3.value == null) {
    number3.value = number
  } else {
    number4.value = number
  }
}

const deleteNumber = function () {
  if (number1.value == null) {
    return
  }

  if (number4.value != null) {
    number4.value = null
  } else if (number3.value != null) {
    number3.value = null
  } else if (number2.value != null) {
    number2.value = null
  } else {
    number1.value = null
  }
}

const clearNumber = function () {
  number1.value = null
  number2.value = null
  number3.value = null
  number4.value = null
}

const goSelect = function () {
  if (number4.value === null) {
    query1.value = true
    clearNumber()
  } else {
    const number = `${number1.value}${number2.value}${number3.value}${number4.value}`

    store.queryCarNumber(number)
    setTimeout(() => {
      if (store.carInfoList !== null) {
        router.push({ name: 'select' })
      } else {
        query2.value = true
        clearNumber()
      }
    }, 100)
  }
}
</script>

<style scoped>
.v-container {
  max-width: none;
}

/* .v-col {
  padding: 0;
} */

.number-box {
  font-size: 7rem;
  font-weight: 700;
  line-height: 1;
  color: black;

  width: 8rem;
  height: 8rem;
  text-align: center;

  border: 8px solid #379777;
  background-color: white;
}

.btn-main {
  width: 6rem !important;
  height: 6rem !important;
  border: 8px solid #FFDD3C;
}

.btn-number {
  font-size: 4rem;
  font-weight: 500;
}

.btn-clear {
  font-size: 3rem;
  font-weight: 500;
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

.bottom-fixed {
  min-height: 120px;
  max-height: 120px;
}

.v-dialog {
  width: 60%;
}

.v-card,
.v-card span {
  text-align: center;

  font-family: 'kcc-hanbit';
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}

.v-card .v-btn {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}
</style>