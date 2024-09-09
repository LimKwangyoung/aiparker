package A104.web_server.service;

import A104.web_server.model.Node;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class DirectionService {

    /**
     * 두 노드 사이의 방향을 계산합니다.
     * @param from 시작 노드
     * @param to 도착 노드
     * @return 방향 (N, S, E, W 중 하나)
     */
    private String getDirection(Node from, Node to) {
        int dx = to.getX() - from.getX();
        int dy = to.getY() - from.getY();

        if (dx == -1 && dy == 0) {
            return "South"; // South
        } else if (dx == 1 && dy == 0) {
            return "North"; // North
        } else if (dx == 0 && dy == 1) {
            return "East"; // East
        } else if (dx == 0 && dy == -1) {
            return "West"; // West
        }
        return "";
    }

    /**
     * 현재 방향과 새로운 방향을 비교하여 상대적인 방향을 계산합니다.
     * @param currentDirection 현재 방향
     * @param newDirection 새로운 방향
     * @return 상대적인 방향 (직진, 우회전, 좌회전, 후진 중 하나)
     */
    private String getRelativeDirection(String currentDirection, String newDirection) {
        if (currentDirection.equals(newDirection)) {
            return "F";
        }

        switch (currentDirection) {
            case "North":
                switch (newDirection) {
                    case "East": return "R";
                    case "West": return "L";
                    case "South": return "B";
                }
                break;
            case "South":
                switch (newDirection) {
                    case "West": return "R";
                    case "East": return "L";
                    case "North": return "B";
                }
                break;
            case "East":
                switch (newDirection) {
                    case "South": return "R";
                    case "North": return "L";
                    case "West": return "B";
                }
                break;
            case "West":
                switch (newDirection) {
                    case "North": return "R";
                    case "South": return "L";
                    case "East": return "B";
                }
                break;
        }

        return "";
    }

    /**
     * 경로를 방향 안내로 변환합니다.
     * @param path 노드 리스트
     * @return 방향 안내 리스트
     */
    public List<String> getDirections(List<Node> path) {
        List<String> directions = new ArrayList<>();
        String currentDirection = "North"; // 초기 방향은 북쪽 (위쪽을 북쪽으로 가정)

        for (int i = 0; i < path.size() - 1; i++) {
            Node from = path.get(i);
            Node to = path.get(i + 1);

            String newDirection = getDirection(from, to);
            String relativeDirection = getRelativeDirection(currentDirection, newDirection);
            if (!relativeDirection.isEmpty()) {
                directions.add(relativeDirection);
            }

            currentDirection = newDirection;
        }

        return directions;
    }
}
