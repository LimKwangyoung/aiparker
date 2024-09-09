import { ref, onMounted, onUnmounted } from 'vue'
import { defineStore } from 'pinia'

export const useMonitorStore = defineStore('monitor', () => {
    const vehicleInfo = ref([])
    const entryInfo = ref([])
    const exitInfo = ref([])

    const occupancyInfo = ref([])

    const occupancyNumber = ref(0)
    const totalPrice = ref(0)

    onMounted(() => {
        const eventSourceVehicles = new EventSource('https://i11a104.p.ssafy.io/api/monitoring/vehicles')
        const eventSourceOccupancy = new EventSource('https://i11a104.p.ssafy.io/api/monitoring/occupancy-status')

        eventSourceVehicles.addEventListener('vehicles', (event) => {
            vehicleInfo.value = JSON.parse(event.data)

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

        eventSourceOccupancy.addEventListener('occupancy-status', (event) => {
            occupancyInfo.value = JSON.parse(event.data)
            occupancyNumber.value = Object.values(occupancyInfo.value).filter(value => value !== null).length
        })
    })

    onUnmounted(() => {
        if (eventSourceVehicles) {
            eventSourceVehicles.close()
        }
        if (eventSourceOccupancy) {
            eventSourceOccupancy.close()
        }
    })
    return { entryInfo, exitInfo, occupancyInfo, occupancyNumber, totalPrice }
}, { persist: true })
