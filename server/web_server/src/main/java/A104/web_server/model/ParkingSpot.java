package A104.web_server.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
public class ParkingSpot {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String code;  // 주차 구역 코드 (예: A1, B2 등)
    private String type; // 일반, 경차, 전기차

    private boolean isOccupied; // 주차 구역 예약
    private boolean isHere; // 실제로 차량이 있는지 없는지

    private int x;  // 주차 구역의 X 좌표
    private int y;  // 주차 구역의 Y 좌표

}
