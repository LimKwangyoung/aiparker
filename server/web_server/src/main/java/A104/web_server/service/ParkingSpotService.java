package A104.web_server.service;

import A104.web_server.controller.MonitoringController;
import A104.web_server.model.Node;
import A104.web_server.model.ParkingSpot;
import A104.web_server.model.Vehicle;
import A104.web_server.repository.ParkingSpotRepository;
import A104.web_server.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class ParkingSpotService {
    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private ParkingSpotRepository parkingSpotRepository;

    @Autowired
    private PathFindingService pathFindingService;

    @Autowired
    private MonitoringController monitoringController;

    // ---------- 주차장 그리드 설정 (false: 장애물, true: 이동 가능)
    private static final boolean[][] grid = {
            {false, true, true, true, true, false},  // 입구 행
            {false, true, true, true, true, false},  // C 행
            {false, false, false, false, false, false},  // 이동 가능한 경로
            {false, true, true, true, true, false},  // B 행
            {false, true, true, true, true, false},  // A 행
            {false, false, false, false, false, false},  // 이동 가능한 경로
            {true, true, true, true, true, true}   // 경차 및 전기차 행
    };

    // 주차 구역별 경로 정보 저장용 맵
    public static final Map<String, List<Object>> PARKING_DIRECTIONS = Map.ofEntries(
            Map.entry("A1", List.of("A1", List.of("F", 114), List.of("R", 5), "parking")),
            Map.entry("A2", List.of("A2", List.of("F", 114), List.of("R", 5), "parking")),
            Map.entry("A3", List.of("A3", List.of("F", 114), List.of("R", 5), "parking")),
            Map.entry("B1", List.of("None", "None", "None", "None")),
            Map.entry("B2", List.of("None", "None", "None", "None")),
            Map.entry("B3", List.of("None", "None", "None", "None")),
            Map.entry("C1", List.of("None", "None", "None", "None")),
            Map.entry("C2", List.of("None", "None", "None", "None")),
            Map.entry("C3", List.of("None", "None", "None", "None")),
            Map.entry("S1", List.of("None", "None", "None", "None")),
            Map.entry("S2", List.of("None", "None", "None", "None")),
            Map.entry("S3", List.of("None", "None", "None", "None")),
            Map.entry("S4", List.of("None", "None", "None", "None")),
            Map.entry("E1", List.of("None", "None", "None", "None")),
            Map.entry("E2", List.of("None", "None", "None", "None"))
    );

    // ---------- 차량의 번호판을 이용해 최적의 주차 경로를 찾습니다.
    public List<Object> findOptimalPathForParkingVer2(String licensePlate) {
        // 차량 정보를 데이터베이스에서 조회
        Vehicle vehicle = vehicleRepository.findByLicensePlate(licensePlate);

        // 차량 유형에 맞는 최적 주차 구역 찾기
        ParkingSpot optimalSpot = findOptimalParkingSpot(vehicle.getType());

        // 주차 구역 까지의 경로 찾기 ver 2
        List<Object> directions = PARKING_DIRECTIONS.get(optimalSpot.getCode());

        // 주차 구역 점유 및 데이터베이스 업데이트
        occupyParkingSpot(vehicle, optimalSpot);

        // 관제 페이지에 알리기
        monitoringController.notifyClients();

        return directions;
    }

    // ---------- 차량의 번호판을 이용해 최적의 주차 경로를 찾습니다.
    public List<Node> findOptimalPathForParking(String licensePlate) {
        // 차량 정보를 데이터베이스에서 조회
        Vehicle vehicle = vehicleRepository.findByLicensePlate(licensePlate);

        // 차량 유형에 맞는 최적 주차 구역 찾기
        ParkingSpot optimalSpot = findOptimalParkingSpot(vehicle.getType());

        // 주차 구역까지의 최적 경로 찾기
        List<Node> path = findPathToParkingSpot(optimalSpot);

        // 주차 구역 점유 및 데이터베이스 업데이트
        occupyParkingSpot(vehicle, optimalSpot);

        // 관제 페이지에 알리기
        monitoringController.notifyClients();

        return path;
    }

    // ---------- 차량 유형에 맞는 최적의 주차 구역을 찾습니다.
    private ParkingSpot findOptimalParkingSpot(String vehicleType) {
        // 사용 가능한 모든 주차 구역 조회
        List<ParkingSpot> availableSpots = parkingSpotRepository.findAllAvailableSpots();

        if (availableSpots.isEmpty()) {
            throw new IllegalStateException("No available parking spots");
        }

        // 차량 유형에 맞는 주차 구역 찾기
        Optional<ParkingSpot> optimalSpot = availableSpots.stream()
                .filter(spot -> spot.getType().equals(vehicleType))
                .sorted(Comparator.comparing(ParkingSpot::getY).thenComparing(ParkingSpot::getX).reversed())
                .findFirst();

        // 특수 주차 구역이 없으면 일반 주차 구역 찾기
        if (!optimalSpot.isPresent()) {
            optimalSpot = availableSpots.stream()
                    .filter(spot -> spot.getType().equals("일반"))
                    .sorted(Comparator.comparing(ParkingSpot::getY).thenComparing(ParkingSpot::getX).reversed())
                    .findFirst();
        }

        return optimalSpot.orElseThrow(() ->
                new IllegalStateException("No available parking spots for vehicle type: " + vehicleType));
    }

    // ---------- 주차 구역까지의 최적 경로를 찾습니다.
    private List<Node> findPathToParkingSpot(ParkingSpot optimalSpot) {
        int startX = 0;  // 출발지 X 좌표 (입구)
        int startY = 0;  // 출발지 Y 좌표 (입구)
        int goalX = optimalSpot.getX();  // 목표지 X 좌표
        int goalY = optimalSpot.getY();  // 목표지 Y 좌표

        // 디버깅 정보 출력
        System.out.println("Start: (" + startX + ", " + startY + ")");
        System.out.println("Goal: (" + goalX + ", " + goalY + ")");

        // 목표 지점의 장애물을 임시로 해제
        boolean originalState = grid[goalX][goalY];
        grid[goalX][goalY] = false;

        // 최적 경로 찾기
        List<Node> path = pathFindingService.findOptimalPath(startX, startY, goalX, goalY, grid);

        // 목표 지점의 장애물을 원래 상태로 복구
        grid[goalX][goalY] = originalState;

        return path;
    }

    // ---------- 주차 구역을 점유하고 데이터베이스를 업데이트합니다.
    private void occupyParkingSpot(Vehicle vehicle, ParkingSpot optimalSpot) {
        // 주차 구역을 점유 상태로 변경
        optimalSpot.setOccupied(true);
        vehicle.setParkingSpot(optimalSpot);

        // 차량 정보 및 주차 구역 정보를 데이터베이스에 저장
        vehicleRepository.save(vehicle);
        vehicleRepository.flush();

        parkingSpotRepository.save(optimalSpot);
        parkingSpotRepository.flush();
    }
}