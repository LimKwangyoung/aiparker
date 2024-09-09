<template>
  <v-container class="pt-15 pb-5 d-flex flex-column">
    <v-row>
      <v-col>
        <v-table class="payment-text mx-auto">
          <tr>
            <td class="py-3 text-white" style="width: 300px;">결제 금액</td>
            <td class="py-3">{{ store.fee }} 원</td>
          </tr>
        </v-table>
      </v-col>
    </v-row>
    <v-row class="mt-5">
      <v-col cols="4">
        <v-card class="text-center mx-5 py-3" elevation="5" rounded="xl" @click=payCard>
          <v-card-item>
            <v-img src="/images/card.png" class="mx-auto"></v-img>
            <v-card-title>
              신용 카드
            </v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="text-center mx-5 py-3" elevation="5" rounded="xl" @click="simpleFlag = true">
          <v-card-item>
            <v-img src="/images/mobile.png" class="mx-auto"></v-img>
            <v-card-title>
              간편 결제
            </v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="4" class="">
        <v-card class="text-center mx-5 py-3" elevation="5" rounded="xl" @click=payCash>
          <v-card-item>
            <v-img src="/images/cash.png" class="mx-auto"></v-img>
            <v-card-title>
              현금 결제
            </v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="bottom-fixed">
      <v-col class="d-flex align-center" cols=4>
        <v-btn class="btn-sub py-3" rounded="xl" @click="goMain">
          <v-icon icon="mdi-home"></v-icon>
        </v-btn>
      </v-col>
      <v-col class="d-flex align-center justify-space-evenly" cols="8">
      </v-col>
    </v-row>

    <v-dialog v-model="cardFlag" persistent>
      <v-card class="py-5" rounded="lg">
        <template v-slot:title>
          <div class="dialog-title">신용 카드를 넣어주세요.</div>
          <div class="dialog-content">결제가 완료될 때까지 카드를 빼지 마세요.</div>
          <v-img src="/images/card-payment.png" class="mx-auto"></v-img>
          <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
        </template>
      </v-card>
    </v-dialog>

    <v-dialog class="simple-dialog" v-model="simpleFlag">
      <v-card class="py-5" rounded="lg">
        <template v-slot:title>
          <div class="dialog-title">결제 수단을 선택해 주세요.</div>
          <v-row class="d-flex justify-center pt-10 pb-5 px-10">
            <v-card class="mx-5 pb-5 elevation-3" @click="paySimple">
              <v-img src="/images/samsungpay.png" class="mx-auto mb-0"></v-img>
              <div class="simple-title">삼성페이</div>
            </v-card>
            <v-card class="mx-5 pb-5 elevation-3" @click="paySimple">
              <v-img src="/images/kakaopay.png" class="mx-auto mb-0"></v-img>
              <div class="simple-title">카카오페이</div>
            </v-card>
            <v-card class="mx-5 pb-5 elevation-3" @click="paySimple">
              <v-img src="/images/naverpay.png" class="mx-auto mb-0"></v-img>
              <div class="simple-title">네이버페이</div>
            </v-card>
          </v-row>
          <v-row class="d-flex justify-center pb-5 px-10">
            <v-card class="mx-5 pb-5 elevation-3" @click="paySimple">
              <v-img src="/images/shpay.png" class="mx-auto mb-0"></v-img>
              <div class="simple-title">신한페이</div>
            </v-card>
            <v-card class="mx-5 pb-5 elevation-3" @click="paySimple">
              <v-img src="/images/kbpay.png" class="mx-auto mb-0"></v-img>
              <div class="simple-title">KB페이</div>
            </v-card>
            <v-card class="mx-5 pb-5 elevation-3" @click="paySimple">
              <v-img src="/images/tosspay.png" class="mx-auto mb-0"></v-img>
              <div class="simple-title">토스페이</div>
            </v-card>
          </v-row>
        </template>
      </v-card>
    </v-dialog>

    <v-dialog v-model="simplePayFlag" persistent>
      <v-card class="py-5" rounded="lg">
        <template v-slot:title>
          <div class="dialog-title mb-15">결제 중입니다.</div>
          <v-img src="/images/simple-payment.png" class="mx-auto mb-15" width="220px"></v-img>
          <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
        </template>
      </v-card>
    </v-dialog>

    <v-dialog v-model="cashFlag" persistent>
      <v-card class="py-5" rounded="lg">
        <template v-slot:title>
          <div class="dialog-title mb-15">현금을 투입하여 주세요.</div>
          <v-img src="/images/cash-payment.png" class="mx-auto"></v-img>
          <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
        </template>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useParkingStore } from '@/stores/parking.js'

const router = useRouter()
const store = useParkingStore()

const cardFlag = ref(false)
const cashFlag = ref(false)
const simpleFlag = ref(false)
const simplePayFlag = ref(false)

const goMain = function () {
  router.push({ name: 'main' })
}

const payCard = function () {
  cardFlag.value = true
  setTimeout(() => {
    cardFlag.value = false
    router.push({ name: 'complete' })
  }, 5000)
}

const paySimple = function () {
  simplePayFlag.value = true
  setTimeout(() => {
    simplePayFlag.value = false
    router.push({ name: 'complete' })
  }, 5000)
}

const payCash = function () {
  cashFlag.value = true
  setTimeout(() => {
    cashFlag.value = false
    router.push({ name: 'complete' })
  }, 5000)
}
</script>

<style scoped>
.v-container {
  max-width: none;
}

/* .v-col {
  padding: 0;
} */

.v-table {
  width: 80%;
  background-color: #379777;

  border: 8px solid #379777;
  border-radius: 8px;
  text-align: center;

  font-size: 3rem;
  font-weight: 300;
  line-height: 1.05;
  letter-spacing: normal;
  text-align: center;
}

.v-table tr :nth-child(2) {
  background-color: white;
}

.v-card {
  background-color: white;
}

.v-row .v-img {
  width: 160px;
  height: 160px;

  margin-bottom: 12px;
}

.v-card-title {
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.015625em
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

.v-dialog {
  width: 55%;
}

.v-dialog .v-img {
  width: 50%;
  margin-bottom: 40px;
}

.v-dialog .v-card {
  text-align: center;
}

.dialog-title {
  font-family: 'kcc-hanbit';
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.0083333333em;

  margin-bottom: 20px;
}

.dialog-content {
  font-family: 'kcc-hanbit';
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.0083333333em;
  color: red;

  margin-bottom: 60px;
}

.simple-dialog {
  width: 70%;
}

.simple-dialog .v-card .v-card {
  min-width: 180px;
}

.simple-title {
  font-family: 'kcc-hanbit';
  font-size: 2rem;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}
</style>