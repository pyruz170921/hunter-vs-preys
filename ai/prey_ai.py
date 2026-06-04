from ai.dijkstra import DijkstraPathfinder
from ai.floyd_warshall import FloydWarshall


class PreyAI:

    @staticmethod
    def free_neighbors_count(graph, position):
        return len(list(graph.neighbors(position)))

    @staticmethod
    def choose_move(
        graph,
        prey_position,
        hunter_position,
        algorithm,
        history=None
    ):
        history = history or []

        neighbors = list(graph.neighbors(prey_position))

        if len(neighbors) == 0:
            return prey_position

        best_position = prey_position
        best_score = -999999

        if algorithm == "DIJKSTRA":
            for position in neighbors:
                distance = DijkstraPathfinder.distance(
                    graph,
                    position,
                    hunter_position
                )

                exits = PreyAI.free_neighbors_count(
                    graph,
                    position
                )

                score = distance + (exits * 2)

                if position in history:
                    score -= 6

                if position == prey_position:
                    score -= 10

                if score > best_score:
                    best_score = score
                    best_position = position

        else:
            dist, _ = FloydWarshall.compute(graph)

            for position in neighbors:
                distance = dist[position][hunter_position]

                exits = PreyAI.free_neighbors_count(
                    graph,
                    position
                )

                score = distance + (exits * 2)

                if position in history:
                    score -= 6

                if position == prey_position:
                    score -= 10

                if score > best_score:
                    best_score = score
                    best_position = position

        return best_position