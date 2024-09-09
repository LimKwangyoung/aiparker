<template>
  <v-app id="app" :style="{ backgroundColor: layout === 'payment' ? '#FFFCEE' : 'white' }">
    <!-- select -->
     <template v-if="layout === 'select'">
      <RouterLink :to="{ name: 'monitoring' }">관제 화면</RouterLink>
      <RouterLink :to="{ name: 'main' }">정산 화면</RouterLink>
     </template>

    <!-- monitoring -->
    <template v-if="layout === 'monitoring'">
      <div class="title d-flex align-center mt-5">
        <v-img src="/images/logo.png" class="main-logo-1 flex-grow-0"></v-img>
        <div class="flex-grow-1">주차장 관제 시스템</div>
      </div>
      <RouterView />
    </template>

    <!-- payment -->
    <template v-if="layout === 'payment'">
      <div class="pt-15 px-10 d-flex flex-column h-100">
        <div>
          <v-img src="/images/logo.png" class="main-logo-2"></v-img>
        </div>
        <RouterView class="flex-grow-1"></RouterView>
      </div>
    </template>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()

const layout = computed(() => {
  if (route.path.startsWith('/monitoring')) {
    return 'monitoring'
  } else if (route.path.startsWith('/payment')) {
    return 'payment'
  }
  return 'select'
})
</script>

<style scoped>
@font-face {
  font-family: 'kcc-hanbit';
  src: url('/fonts/KCC-Hanbit.ttf');
}

#app {
  font-family: 'kcc-hanbit';
}

.main-logo-1 {
  width: 350px;
}

.title {
  font-size: 2.3rem;
  font-weight: 600;
  line-height: 1;
  letter-spacing: -0.015625em;
  
  height: 75px;
}

.main-logo-2 {
  width: 600px;
  margin-left: auto;
  margin-right: auto;
}
</style>