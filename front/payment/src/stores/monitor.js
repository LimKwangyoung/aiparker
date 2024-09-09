import { ref, onMounted, onUnmounted, watch } from 'vue'
import { defineStore } from 'pinia'

import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)

export const useMonitorStore = defineStore('monitor', () => {
    const vehicleInfo = ref([])
    const entryInfo = ref([])
    const exitInfo = ref([])

    const entrySortInfo = ref([])
    const exitSortArray = ref([])

    const occupancyInfo = ref([])

    const occupancyNumber = ref(0)
    const totalPrice = ref(0)

    const eventSourceVehicles = ref(null)
    const eventSourceOccupancy = ref(null)

    onMounted(() => {
        eventSourceVehicles.value = new EventSource('https://i11a104.p.ssafy.io/api/monitoring/vehicles')
        eventSourceOccupancy.value = new EventSource('https://i11a104.p.ssafy.io/api/monitoring/occupancy-status')

        eventSourceVehicles.value.addEventListener('vehicles', (event) => {
            vehicleInfo.value = JSON.parse(event.data)

            vehicleInfo.value.forEach(element => {
                if (element.entryTime) {
                    element.entryTime = dayjs.utc(element.entryTime).tz('Asia/Seoul').format('YYYY-MM-DD HH:mm:ss')
                }
                if (element.exitTime) {
                    element.exitTime = dayjs.utc(element.exitTime).tz('Asia/Seoul').format('YYYY-MM-DD HH:mm:ss')
                }
            })

            totalPrice.value = 0
            vehicleInfo.value.forEach(element => {
                totalPrice.value += element.fee
            })
            entryInfo.value = vehicleInfo.value.filter((element) => {
                return element['entryTime'] !== null
            })
            exitInfo.value = vehicleInfo.value.filter((element) => {
                return element['exitTime'] !== null
            })
        })

        eventSourceOccupancy.value.addEventListener('occupancy-status', (event) => {
            occupancyInfo.value = JSON.parse(event.data)
            occupancyNumber.value = Object.values(occupancyInfo.value).filter(value => value !== null).length
        })
    })

    onUnmounted(() => {
        if (eventSourceVehicles.value) {
            eventSourceVehicles.value.close()
        }
        if (eventSourceOccupancy.value) {
            eventSourceOccupancy.value.close()
        }
    })

    watch(entryInfo, (newValue) => {
        entrySortInfo.value = [...newValue].sort((a, b) => new Date(a.entryTime) - new Date(b.entryTime))
    }, { deep: true })

    watch(exitInfo, (newValue) => {
        exitSortArray.value = [...newValue].sort((a, b) => new Date(a.exitTime) - new Date(b.exitTime))
    }, { deep: true })
    
    return { entryInfo, exitInfo, entrySortInfo, exitSortArray, occupancyInfo, occupancyNumber, totalPrice }
}, { persist: true })
