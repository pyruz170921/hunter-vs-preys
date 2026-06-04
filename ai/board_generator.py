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

        min_distance = cls.MIN_DISTANCES[size]
    
        while True:
        
            total_cells = size * size
    
            obstacle_count = int(
                total_cells * cls.OBSTACLE_PERCENTAGE
            )
    
            all_positions = [
                (x, y)
                for x in range(size)
                for y in range(size)
            ]
    
            random.shuffle(all_positions)
    
            hunter = all_positions.pop()
    
            preys = []
    
            while len(preys) < cls.PREY_COUNT:
            
                candidate = all_positions.pop()
    
                if (
                    cls.manhattan(
                        hunter,
                        candidate
                    ) >= min_distance
                ):
                    preys.append(candidate)
    
            obstacles = set()
    
            while len(obstacles) < obstacle_count:
            
                pos = random.choice(all_positions)
    
                if (
                    pos != hunter
                    and pos not in preys
                ):
                    obstacles.add(pos)
    
            graph = GridGraph(
                size,
                obstacles
            )
    
            valid = (
                ConnectivityValidator
                .validate_board(
                    graph,
                    hunter,
                    preys
                )
            )
    
            if valid:
            
                return {
                    "size": size,
                    "hunter": hunter,
                    "preys": preys,
                    "obstacles": list(obstacles)
                }