<template>
  <v-container class="px-13 py-10">
    <v-row>
      <v-col cols="4">
        <InformationVue />
      </v-col>
      <v-col cols="5">
        <ParkingLotVue />
      </v-col>
      <v-col cols="3">
        <CalculateVue />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import InformationVue from '@/components/InformationVue.vue'
import ParkingLotVue from '@/components/ParkingLotVue.vue'
import CalculateVue from '@/components/CalculateVue.vue'
</script>

<style scoped>
.v-container {
  max-width: none;
  padding: 0;
}
</style>