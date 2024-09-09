import { ref } from 'vue'
import { defineStore } from 'pinia'

import axios from 'axios'

export const useParkingStore = defineStore('parking', () => {
  const carInfoList = ref(null)
  const carNumber = ref(null)
  const carInfo = ref(null)

  const exitTime = ref(null)
  const fee = ref(0)

  const queryCarNumber = function (number) {
    const response = ref(null)

    axios({
      url: `https://i11a104.p.ssafy.io/api/payment/vehicles?licensePlateEnd=${number}`,
      // url: `http://i11a104.p.ssafy.io:8000/api/payment/vehicles?licensePlateEnd=${number}`,
      method: 'get'
    })
      .then(res => {
        response.value = res['data']

        if (Object.keys(response.value).length > 0) {
          carInfoList.value = response.value.filter(carInfo => {
            return carInfo.licensePlate.slice(-4) == number
          })
        }
        else {
          carInfoList.value = null
        }
      })
      .catch(err => {
        console.log(err)
      })
  }

  const saveCarNumber = function (number) {
    carNumber.value = number
    carInfo.value = carInfoList.value.find(carInfo => carInfo.licensePlate === number)
  }

  return { carInfoList, carNumber, carInfo, exitTime, fee, queryCarNumber, saveCarNumber }
}, { persist: true })
