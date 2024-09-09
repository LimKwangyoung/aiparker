package A104.web_server.dto;

import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter

public class PaymentRequestDTO {
    @Id
    private Long id;

//    private String licensePlate;
//    private String type; // 일반, 경차, 전기차
//    private LocalDateTime entryTime;
    private LocalDateTime exitTime;
    private Integer fee;
}
