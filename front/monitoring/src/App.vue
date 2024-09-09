<template>
  <v-app id="app">
      <div class="title d-flex align-center mt-5">
        <v-img src="/images/logo.png" class="main-logo flex-grow-0"></v-img>
        <div class="flex-grow-1">주차장 관제 시스템</div>
      </div>
      <MainVue></MainVue>
  </v-app>
</template>

<script setup>
import MainVue from '@/components/MainVue.vue'
</script>

<style scoped>
@font-face {
  font-family: 'kcc-hanbit';
  src: url('/fonts/KCC-Hanbit.ttf');
}

#app {
  font-family: 'kcc-hanbit';
}

.main-logo {
  width: 350px;
}

.title {
  font-size: 2.3rem;
  font-weight: 600;
  line-height: 1;
  letter-spacing: -0.015625em;
  
  height: 75px;
}
</style>