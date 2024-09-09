package A104.web_server.service;

import A104.web_server.model.ParkingSpot;
import A104.web_server.model.Vehicle;
import A104.web_server.repository.ParkingSpotRepository;
import A104.web_server.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class MonitoringService {
    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private ParkingSpotRepository parkingSpotRepository;

    // 차량 내역 조회
    public List<Vehicle> getAllVehicles() {
         return vehicleRepository.findAll();
    }

    // 주차 구역 조회
    public List<ParkingSpot> getAllParkingSpots() {
        return parkingSpotRepository.findAll();
    }

    // 주차장 점유 현황 조회
    public Map<String, Object> getOccupancyStatus() {
        List<ParkingSpot> parkingSpots = parkingSpotRepository.findAll();
        Map<String, Object> occupancyStatus = new HashMap<>();

        for (ParkingSpot spot : parkingSpots) {
            String licensePlate = null;
            Optional<Vehicle> vehicle = vehicleRepository.findByParkingSpot(spot);
            if (vehicle.isPresent()) {
                licensePlate = vehicle.get().getLicensePlate();
            }
            occupancyStatus.put(spot.getCode(), licensePlate);
        }

        return occupancyStatus;
    }
}
