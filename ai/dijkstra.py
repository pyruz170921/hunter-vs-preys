import heapq


class DijkstraPathfinder:

    @staticmethod
    def shortest_path(
        graph,
        start,
        target
    ):

        queue = []

        heapq.heappush(
            queue,
            (0, start)
        )

        distances = {
            start: 0
        }

        previous = {}

        visited = set()

        while queue:

            current_distance, current_node = (
                heapq.heappop(queue)
            )

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == target:
                break

            for neighbor in graph.neighbors(
                current_node
            ):

                distance = (
                    current_distance + 1
                )

                if (
                    neighbor not in distances
                    or
                    distance <
                    distances[neighbor]
                ):

                    distances[neighbor] = distance

                    previous[neighbor] = (
                        current_node
                    )

                    heapq.heappush(
                        queue,
                        (
                            distance,
                            neighbor
                        )
                    )

        if target not in distances:
            return []

        path = []

        current = target

        while current != start:

            path.append(current)

            current = previous[current]

        path.append(start)

        path.reverse()

        return path
    
    @staticmethod
    def distance(
        graph,
        start,
        target
    ):

        path = DijkstraPathfinder.shortest_path(
            graph,
            start,
            target
        )

        if not path:
            return float("inf")

        return len(path) - 1