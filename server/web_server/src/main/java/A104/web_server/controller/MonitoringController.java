package A104.web_server.controller;

import A104.web_server.model.ParkingSpot;
import A104.web_server.model.Vehicle;
import A104.web_server.service.MonitoringService;
import A104.web_server.service.ParkingSpotService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@RestController
@RequestMapping("/api/monitoring")
public class MonitoringController {
    private final MonitoringService monitoringService;
    private final List<SseEmitter> vehicleEmitters = new CopyOnWriteArrayList<>();
    private final List<SseEmitter> parkingSpotEmitters = new CopyOnWriteArrayList<>();
    private final List<SseEmitter> occupancyStatusEmitters = new CopyOnWriteArrayList<>();
    private final ExecutorService executor = Executors.newCachedThreadPool();

    public MonitoringController(MonitoringService monitoringService) {
        this.monitoringService = monitoringService;
    }

    // 차량 내역 조회 API (SSE)
    @GetMapping("/vehicles")
    public SseEmitter getAllVehiclesSse() {
        SseEmitter emitter = new SseEmitter();
        vehicleEmitters.add(emitter);
        executor.execute(() -> {
            try {
                List<Vehicle> vehicles = monitoringService.getAllVehicles();
                emitter.send(SseEmitter.event().name("vehicles").data(vehicles));
                emitter.complete();
            } catch (IOException e) {
                emitter.completeWithError(e);
            } finally {
                vehicleEmitters.remove(emitter);
            }
        });
        return emitter;
    }

    // 주차 구역 조회 API (SSE)
    @GetMapping("/parking-spots")
    public SseEmitter getAllParkingSpotsSse() {
        SseEmitter emitter = new SseEmitter();
        parkingSpotEmitters.add(emitter);
        executor.execute(() -> {
            try {
                List<ParkingSpot> parkingSpots = monitoringService.getAllParkingSpots();
                emitter.send(SseEmitter.event().name("parking-spots").data(parkingSpots));
                emitter.complete();
            } catch (IOException e) {
                emitter.completeWithError(e);
            } finally {
                parkingSpotEmitters.remove(emitter);
            }
        });
        return emitter;
    }

    // 주차장 점유 현황 조회 API (SSE)
    @GetMapping("/occupancy-status")
    public SseEmitter getOccupancyStatusSse() {
        SseEmitter emitter = new SseEmitter();
        occupancyStatusEmitters.add(emitter);
        executor.execute(() -> {
            try {
                Map<String, Object> occupancyStatus = monitoringService.getOccupancyStatus();
                emitter.send(SseEmitter.event().name("occupancy-status").data(occupancyStatus));
                emitter.complete();
            } catch (IOException e) {
                emitter.completeWithError(e);
            } finally {
                occupancyStatusEmitters.remove(emitter);
            }
        });
        return emitter;
    }

    // 클라이언트에 실시간으로 알림을 보내는 메서드
    public void notifyClients() {
        for (SseEmitter emitter : vehicleEmitters) {
            try {
                List<Vehicle> vehicles = monitoringService.getAllVehicles();
                emitter.send(SseEmitter.event().name("vehicles").data(vehicles));
            } catch (IOException e) {
                emitter.completeWithError(e);
                vehicleEmitters.remove(emitter);
            }
        }

        for (SseEmitter emitter : parkingSpotEmitters) {
            try {
                List<ParkingSpot> parkingSpots = monitoringService.getAllParkingSpots();
                emitter.send(SseEmitter.event().name("parking-spots").data(parkingSpots));
            } catch (IOException e) {
                emitter.completeWithError(e);
                parkingSpotEmitters.remove(emitter);
            }
        }

        for (SseEmitter emitter : occupancyStatusEmitters) {
            try {
                Map<String, Object> occupancyStatus = monitoringService.getOccupancyStatus();
                emitter.send(SseEmitter.event().name("occupancy-status").data(occupancyStatus));
            } catch (IOException e) {
                emitter.completeWithError(e);
                occupancyStatusEmitters.remove(emitter);
            }
        }
    }
}
