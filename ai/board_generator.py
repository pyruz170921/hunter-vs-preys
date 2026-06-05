import random

from ai.graph import GridGraph
from ai.connectivity import ConnectivityValidator


class BoardGenerator:
    OBSTACLE_PERCENTAGE = 0.30
    PREY_COUNT = 4

    MIN_DISTANCES = {
        8: 4,
        10: 5,
        12: 6,
        15: 8,
    }

    @staticmethod
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @classmethod
    def generate(cls, size):
        min_distance = cls.MIN_DISTANCES.get(size, 4)

        while True:
            total_cells = size * size
            obstacle_count = int(total_cells * cls.OBSTACLE_PERCENTAGE)

            all_positions = [
                (x, y)
                for x in range(size)
                for y in range(size)
            ]

            random.shuffle(all_positions)

            hunter = all_positions.pop()

            preys = []

            available_for_preys = all_positions.copy()
            random.shuffle(available_for_preys)

            for candidate in available_for_preys:
                if len(preys) >= cls.PREY_COUNT:
                    break

                if cls.manhattan(hunter, candidate) >= min_distance:
                    preys.append(candidate)

            if len(preys) < cls.PREY_COUNT:
                continue

            blocked_positions = set(preys)
            blocked_positions.add(hunter)

            available_for_obstacles = [
                position
                for position in all_positions
                if position not in blocked_positions
            ]

            random.shuffle(available_for_obstacles)

            obstacles = set(
                available_for_obstacles[:obstacle_count]
            )

            graph = GridGraph(
                size,
                obstacles
            )

            valid = ConnectivityValidator.validate_board(
                graph,
                hunter,
                preys
            )

            if valid:
                return {
                    "size": size,
                    "hunter": hunter,
                    "preys": preys,
                    "obstacles": list(obstacles),
                }