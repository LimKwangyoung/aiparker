<template>
  <v-container class="pt-15 pb-5 d-flex flex-column">
    <v-row class="title justify-center">
      본인 차량 확인 후 선택해주시기 바랍니다.
    </v-row>
    <v-row>
      <v-sheet class="d-flex justify-center">
        <v-slide-group show-arrows>
          <v-slide-group-item v-for="carInfo in store.carInfoList">
            <v-card class="mx-5 my-5 text-center" elevation="5" rounded="xl" @click="goDetail(carInfo['licensePlate'])">
              <v-card-item>
                <!-- <v-img src="/images/empty.png" class="mx-auto pb-5"></v-img> -->
                <!-- <ImageVue :img-src="carInfo['s3']" class="mx-auto my-5" /> -->
                <v-img :src="carInfo['s3']" class="mx-auto my-5"></v-img>
                <v-card-title>
                  {{ carInfo['licensePlate'].slice(0, -4) }} {{ carInfo['licensePlate'].slice(-4) }}
                </v-card-title>
              </v-card-item>
            </v-card>
          </v-slide-group-item>
          <!-- <v-slide-group-item v-if="Object.keys(store.carInfoList).length === 1">
            <v-card class="mx-5 my-5 text-center" elevation="5" rounded="xl">
              <v-card-item>
                <v-img src="/images/empty.png" class="mx-auto pb-5"></v-img>
              </v-card-item>
            </v-card>
          </v-slide-group-item> -->
        </v-slide-group>
      </v-sheet>
    </v-row>
    <v-row class="bottom-fixed">
      <v-col class="d-flex align-center">
        <v-btn class="btn-sub py-3" rounded="xl" @click="goMain">
          <v-icon icon="mdi-home"></v-icon>
        </v-btn>
      </v-col>
      <v-col class="d-flex justify-end align-center">
        <v-btn class="btn-sub py-3" rounded="xl" @click="goBack">이전으로</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useParkingStore } from '@/stores/parking.js'

// import ImageVue from '@/components/ImageVue.vue'

const router = useRouter()
const store = useParkingStore()

const goDetail = function (number) {
  store.saveCarNumber(number)
  router.push({ name: 'detail' })
}

const goMain = function () {
  router.push({ name: 'main' })
}

const goBack = function () {
  router.push({ name: 'input' })
}
</script>

<style scoped>
.v-container {
  max-width: none;
}

/* .v-col {
  padding: 0;
} */

.title {
  font-size: 3rem;
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}

.v-sheet {
  width: 100%;

  background-color: #FFFCEE;
}

:v-deep .v-slide-group__content {
  justify-content: center !important;
}

.v-card {
  width: 330px;

  background-color: whitesmoke;
}

/* .v-img {
  width: 250px;
  height: 250px;
} */

.v-card-title {
  font-size: 3.5rem;
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
</style>