class GridGraph:

    def __init__(self, size, obstacles):

        self.size = size

        self.obstacles = set(obstacles)

        self.graph = {}

        self.build()

    def build(self):

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for x in range(self.size):

            for y in range(self.size):

                node = (x, y)

                if node in self.obstacles:
                    continue

                self.graph[node] = []

                for dx, dy in directions:

                    nx = x + dx
                    ny = y + dy

                    neighbor = (nx, ny)

                    if (
                        0 <= nx < self.size
                        and 0 <= ny < self.size
                        and neighbor not in self.obstacles
                    ):
                        self.graph[node].append(neighbor)

    def neighbors(self, node):

        return self.graph.get(node, [])

    def nodes(self):

        return list(self.graph.keys())