from collections import deque


class ConnectivityValidator:

    @staticmethod
    def path_exists(graph, start, target):

        visited = set()

        queue = deque([start])

        while queue:

            current = queue.popleft()

            if current == target:
                return True

            if current in visited:
                continue

            visited.add(current)

            for neighbor in graph.neighbors(current):

                if neighbor not in visited:
                    queue.append(neighbor)

        return False

    @classmethod
    def validate_board(
        cls,
        graph,
        hunter,
        preys
    ):

        for prey in preys:

            if not cls.path_exists(
                graph,
                hunter,
                prey
            ):
                return False

        return True