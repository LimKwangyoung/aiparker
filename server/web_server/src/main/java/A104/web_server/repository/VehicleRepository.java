package A104.web_server.repository;

import A104.web_server.model.ParkingSpot;
import A104.web_server.model.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VehicleRepository  extends JpaRepository<Vehicle, Long> {
    Vehicle findByLicensePlate(@Param("licensePlate") String licensePlate);

    Optional<Vehicle> findByParkingSpot(ParkingSpot parkingSpot);

    List<Vehicle> findByLicensePlateEndingWithAndExitTimeIsNull(String licensePlateEnd);

}
