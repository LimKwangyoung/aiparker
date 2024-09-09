package A104.web_server.model;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Node {
    private int x, y;
    private double g, h;
    private Node parent;

    public Node(int x, int y, double g, double h, Node parent) {
        this.x = x;
        this.y = y;
        this.g = g;
        this.h = h;
        this.parent = parent;
    }

    public double getF() {
        return g + h;
    }

}
