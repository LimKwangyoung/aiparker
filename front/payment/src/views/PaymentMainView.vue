<template>
  <div class="d-flex flex-column justify-space-evenly align-center">
    <div class="current-time">
      <div class="date text-center">{{ month }}월 {{ day }}일</div>
      <div class="time">{{ hour }} : {{ minute }} : {{ second }}</div>
    </div>
    <v-btn @click="goInput" class="px-10 py-5" rounded="xl">정산하기</v-btn>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const date = ref(null)
const month = ref(null)
const day = ref(null)
const hour = ref(null)
const minute = ref(null)
const second = ref(null)

const router = useRouter()

onMounted(() => {
  setInterval(() => {
    date.value = new Date()
    month.value = date.value.getMonth() + 1
    day.value = date.value.getDate()
    hour.value = date.value.getHours().toString().padStart(2, '0')
    minute.value = date.value.getMinutes().toString().padStart(2, '0')
    second.value = date.value.getSeconds().toString().padStart(2, '0')
  }, 1)
})

const goInput = function () {
  router.push({ name: 'input' })
}
</script>

<style scoped>
.date {
  font-size: 5rem;
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.0083333333em;
}

.time {
  font-size: 10rem;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.015625em
}

.v-btn {
  height: auto !important;

  font-size: 4rem;
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.0083333333em;
  color: white;

  background-color: #379777;
}
</style>