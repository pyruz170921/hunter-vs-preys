class FloydWarshall:

    @staticmethod
    def compute(graph):

        nodes = graph.nodes()

        dist = {}

        next_node = {}

        for i in nodes:

            dist[i] = {}

            next_node[i] = {}

            for j in nodes:

                if i == j:

                    dist[i][j] = 0

                else:

                    dist[i][j] = float("inf")

        for node in nodes:

            for neighbor in graph.neighbors(node):

                dist[node][neighbor] = 1

                next_node[node][neighbor] = neighbor

        for k in nodes:

            for i in nodes:

                for j in nodes:

                    if (
                        dist[i][k]
                        + dist[k][j]
                        <
                        dist[i][j]
                    ):

                        dist[i][j] = (
                            dist[i][k]
                            + dist[k][j]
                        )

                        next_node[i][j] = (
                            next_node[i].get(k)
                        )

        return dist, next_node
    
    @staticmethod
    def shortest_path(
        start,
        target,
        next_node
    ):

        if (
            start not in next_node
            or
            target not in next_node[start]
        ):
            return []

        path = [start]

        while start != target:

            start = next_node[start][target]

            path.append(start)

        return path