package A104.web_server.controller;

import A104.web_server.dto.PaymentRequestDTO;
import A104.web_server.model.Vehicle;
import A104.web_server.service.PaymentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/payment")
public class PaymentController {

    private final PaymentService paymentService;

    public PaymentController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    // 주차 번호에 따른 차량 정보 조회 API
    @GetMapping("/vehicles")
    public ResponseEntity<List<Vehicle>> getVehiclesByLicensePlateEnd(@RequestParam("licensePlateEnd") String licensePlateEnd) {
        List<Vehicle> vehicles = paymentService.getVehiclesByLicensePlateEnd(licensePlateEnd);
        return ResponseEntity.ok(vehicles);
    }

    // 정산 완료 API
    @PostMapping("/complete")
    public ResponseEntity<String> completePayment(@RequestBody PaymentRequestDTO paymentRequest) {
        paymentService.completePayment(paymentRequest);
        return ResponseEntity.ok("Payment completed");
    }
}
