package A104.web_server.service;

import A104.web_server.model.Node;
import A104.web_server.model.ParkingSpot;
import A104.web_server.repository.ParkingSpotRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
public class ParkingSpotServiceTest {
    @Autowired
    private ParkingSpotRepository parkingSpotRepository;

    @Autowired
    private ParkingSpotService parkingSpotService;

    @Test
    public void testFindAllParkingSpots() {
        // Retrieve all parking spots
        List<ParkingSpot> parkingSpots = parkingSpotRepository.findAll();

        // Assert that the correct number of parking spots are retrieved
        assertThat(parkingSpots).hasSize(15);

        // Print out the parking spots to verify
        parkingSpots.forEach(spot -> {
            System.out.println("Code: " + spot.getCode() + ", Type: " + spot.getType() + ", X: " + spot.getX() + ", Y: " + spot.getY());
        });
    }

    @Test
    public void testFindOptimalPathForParking() {
        // 예시로 경차 타입 차량의 최적 경로 찾기
        List<Node> path = parkingSpotService.findOptimalPathForParking("경차");

        // Assert that a path is found
        assertThat(path).isNotEmpty();

        // Print out the path to verify
        path.forEach(node -> {
            System.out.println("X: " + node.getX() + ", Y: " + node.getY());
        });
    }

    @Test
    public void testFindOptimalPathForElectricVehicle() {
        // 예시로 전기차 타입 차량의 최적 경로 찾기
        List<Node> path = parkingSpotService.findOptimalPathForParking("전기차");

        // Assert that a path is found
        assertThat(path).isNotEmpty();

        // Print out the path to verify
        path.forEach(node -> {
            System.out.println("X: " + node.getX() + ", Y: " + node.getY());
        });
    }

    @Test
    public void testFindOptimalPathForGeneralVehicle() {
        // 예시로 일반 차량의 최적 경로 찾기
        List<Node> path = parkingSpotService.findOptimalPathForParking("일반");

        // Assert that a path is found
        assertThat(path).isNotEmpty();

        // Print out the path to verify
        path.forEach(node -> {
            System.out.println("X: " + node.getX() + ", Y: " + node.getY());
        });
    }

}
