package A104.web_server.repository;

import A104.web_server.model.ParkingSpot;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ParkingSpotRepository extends JpaRepository<ParkingSpot, Long> {
    // 특정 타입의 이용 가능한 주차 공간을 찾는 쿼리
    @Query("SELECT p FROM ParkingSpot p WHERE p.isOccupied = false AND p.isHere = false AND p.type = :type")
    List<ParkingSpot> findAvailableSpotsByType(@Param("type") String type);

    // 모든 이용 가능한 주차 공간을 찾는 쿼리
    @Query("SELECT p FROM ParkingSpot p WHERE p.isOccupied = false AND p.isHere = false")
    List<ParkingSpot> findAllAvailableSpots();
}