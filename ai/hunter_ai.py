from ai.dijkstra import DijkstraPathfinder
from ai.floyd_warshall import FloydWarshall


class HunterAI:

    @staticmethod
    def choose_target(
        graph,
        hunter_position,
        prey_positions,
        algorithm
    ):
        closest_prey = None
        shortest_distance = float("inf")

        if algorithm == "DIJKSTRA":
            for prey in prey_positions:
                distance = DijkstraPathfinder.distance(
                    graph,
                    hunter_position,
                    prey
                )

                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_prey = prey

        else:
            dist, _ = FloydWarshall.compute(graph)

            for prey in prey_positions:
                distance = dist[hunter_position][prey]

                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_prey = prey

        return closest_prey

    @staticmethod
    def next_move(
        graph,
        hunter_position,
        prey_positions,
        algorithm
    ):
        target = HunterAI.choose_target(
            graph,
            hunter_position,
            prey_positions,
            algorithm
        )

        if not target:
            return hunter_position

        if algorithm == "DIJKSTRA":
            path = DijkstraPathfinder.shortest_path(
                graph,
                hunter_position,
                target
            )
        else:
            _, next_node = FloydWarshall.compute(graph)

            path = FloydWarshall.shortest_path(
                hunter_position,
                target,
                next_node
            )

        if len(path) > 1:
            return path[1]

        return hunter_position