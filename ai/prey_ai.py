from ai.dijkstra import DijkstraPathfinder
from ai.floyd_warshall import FloydWarshall


class PreyAI:

    @staticmethod
    def choose_move(
        graph,
        prey_position,
        hunter_position,
        algorithm,
        history=None
    ):
        history = history or []

        best_position = prey_position
        best_score = -1

        neighbors = list(graph.neighbors(prey_position))
        neighbors.append(prey_position)

        if algorithm == "DIJKSTRA":
            for position in neighbors:
                score = DijkstraPathfinder.distance(
                    graph,
                    position,
                    hunter_position
                )

                if position in history:
                    score -= 5

                if score > best_score:
                    best_score = score
                    best_position = position

        else:
            dist, _ = FloydWarshall.compute(graph)

            for position in neighbors:
                score = dist[position][hunter_position]

                if position in history:
                    score -= 5

                if score > best_score:
                    best_score = score
                    best_position = position

        return best_position