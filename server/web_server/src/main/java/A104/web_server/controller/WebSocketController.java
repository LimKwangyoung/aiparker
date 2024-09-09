package A104.web_server.controller;

import A104.web_server.model.Node;
import A104.web_server.model.Vehicle;
import A104.web_server.service.DirectionService;
import A104.web_server.service.ParkingSpotService;
import A104.web_server.service.PathFindingService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

@Component
public class WebSocketController extends TextWebSocketHandler {

    private final ParkingSpotService parkingSpotService;
    private final DirectionService directionService;
    private final ObjectMapper objectMapper;

    public WebSocketController(ParkingSpotService parkingSpotService, DirectionService directionService) {
        this.parkingSpotService = parkingSpotService;
        this.directionService = directionService;
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        System.out.println("Connected: " + session.getId());
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String payload = message.getPayload();
        System.out.println("Received: " + payload);

        // 클라이언트로부터 차량 번호판을 수신
        Map<String, String> data = objectMapper.readValue(payload, Map.class);
        String licensePlate = data.get("licensePlate");

        // 최적 경로 계산
        // List<Node> path = parkingSpotService.findOptimalPathForParking(licensePlate);
        List<Object> directions = parkingSpotService.findOptimalPathForParkingVer2(licensePlate);

        // 경로를 방향 안내로 변환
        // List<String> directions = directionService.getDirections(path);

        // 방향 안내를 JSON 형식으로 변환
        String directionsJson = objectMapper.writeValueAsString(directions);

        // 클라이언트로 방향 안내 전송
        session.sendMessage(new TextMessage(directionsJson));
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        System.out.println("Disconnected: " + session.getId());
    }
}
