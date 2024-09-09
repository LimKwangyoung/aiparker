package A104.web_server.service;

import A104.web_server.model.Node;
import A104.web_server.model.ParkingSpot;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class PathFindingService {

    private static final int[][] DIRECTIONS = {
            {0, 1}, {1, 0}, {0, -1}, {-1, 0}, // 상하좌우
    };

    public List<Node> findOptimalPath(int startX, int startY, int goalX, int goalY, boolean[][] grid) {
        PriorityQueue<Node> openList = new PriorityQueue<>(Comparator.comparingDouble(Node::getF));
        Set<Node> closedList = new HashSet<>();

        Node startNode = new Node(startX, startY, 0, getHeuristic(startX, startY, goalX, goalY), null);
        openList.add(startNode);

        while (!openList.isEmpty()) {
            Node current = openList.poll();
            if (current.getX() == goalX && current.getY() == goalY) {
                return reconstructPath(current);
            }

            closedList.add(current);

            for (int[] direction : DIRECTIONS) {
                int neighborX = current.getX() + direction[0];
                int neighborY = current.getY() + direction[1];

                if (isValid(neighborX, neighborY, grid) && !isInClosedList(neighborX, neighborY, closedList)) {
                    double tentativeG = current.getG() + 1;
                    Node neighbor = new Node(neighborX, neighborY, tentativeG, getHeuristic(neighborX, neighborY, goalX, goalY), current);

                    if (!isInOpenList(neighbor, openList) || tentativeG < neighbor.getG()) {
                        openList.add(neighbor);
                    }
                }
            }
        }
        return Collections.emptyList(); // 경로를 찾지 못함
    }

    private boolean isValid(int x, int y, boolean[][] grid) {
        return x >= 0 && y >= 0 && x < grid.length && y < grid[0].length && !grid[x][y];
    }

    private boolean isInClosedList(int x, int y, Set<Node> closedList) {
        return closedList.stream().anyMatch(node -> node.getX() == x && node.getY() == y);
    }

    private boolean isInOpenList(Node node, PriorityQueue<Node> openList) {
        return openList.stream().anyMatch(n -> n.getX() == node.getX() && n.getY() == node.getY());
    }

    private double getHeuristic(int x1, int y1, int x2, int y2) {
        return Math.abs(x1 - x2) + Math.abs(y1 - y2); // 맨해튼 거리
    }

    private List<Node> reconstructPath(Node node) {
        List<Node> path = new ArrayList<>();
        while (node != null) {
            path.add(node);
            node = node.getParent();
        }
        Collections.reverse(path);
        return path;
    }

}
