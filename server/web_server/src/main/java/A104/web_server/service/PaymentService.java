package A104.web_server.service;

import A104.web_server.controller.MonitoringController;
import A104.web_server.dto.PaymentRequestDTO;
import A104.web_server.model.ParkingSpot;
import A104.web_server.model.Vehicle;
import A104.web_server.repository.ParkingSpotRepository;
import A104.web_server.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PaymentService {
    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private ParkingSpotRepository parkingSpotRepository;

    @Autowired
    private MonitoringController monitoringController;

    // 주차 번호에 따른 차량 정보 조회
    public List<Vehicle> getVehiclesByLicensePlateEnd(String licensePlateEnd) {
        return vehicleRepository.findByLicensePlateEndingWithAndExitTimeIsNull(licensePlateEnd);
    }

    // 정산 완료
    public void completePayment(PaymentRequestDTO paymentRequest) {
        Optional<Vehicle> vehicleOptional = vehicleRepository.findById(paymentRequest.getId());
        if (vehicleOptional.isPresent()) {

            Vehicle vehicle = vehicleOptional.get();
            ParkingSpot parkingSpot = vehicle.getParkingSpot();

            // 정산금 저장
            vehicle.setExitTime(paymentRequest.getExitTime());
            vehicle.setFee(paymentRequest.getFee());

            // 주차장 점유 해제
            setFreeParkingSpot(vehicle, parkingSpot);

            // 관제 페이지에 알리기
            monitoringController.notifyClients();
        }

    }

    // ---------- 주차 구역을 점유 해제하고 데이터베이스를 업데이트합니다.
    private void setFreeParkingSpot(Vehicle vehicle, ParkingSpot parkingSpot) {
        // 주차 구역을 점유 해제 상태로 변경
        parkingSpot.setOccupied(false);
        vehicle.setParkingSpot(null);

        // 차량 정보 및 주차 구역 정보를 데이터베이스에 저장
        vehicleRepository.save(vehicle);
        vehicleRepository.flush();

        parkingSpotRepository.save(parkingSpot);
        parkingSpotRepository.flush();
    }
}
