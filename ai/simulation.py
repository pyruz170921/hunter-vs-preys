from ai.board_generator import BoardGenerator
from ai.graph import GridGraph
from ai.hunter_ai import HunterAI
from ai.prey_ai import PreyAI
from game.models import (
    Game,
    Board,
    Obstacle,
    Hunter,
    Prey,
    GameEvent,
    Movement,
)

class SimulationEngine:

    def __init__(self, board_size, hunter_algorithm):
        self.board = BoardGenerator.generate(board_size)

        self.graph = GridGraph(
            self.board["size"],
            self.board["obstacles"]
        )

        self.hunter_algorithm = hunter_algorithm

        self.prey_algorithm = (
            "FLOYD"
            if hunter_algorithm == "DIJKSTRA"
            else "DIJKSTRA"
        )

        self.hunter = self.board["hunter"]

        self.preys = [
            {
                "id": index + 1,
                "position": prey,
                "alive": True,
                "moves": 0,
                "survival_time": 0,
                "captured_at": None,
                "history": []
            }
            for index, prey in enumerate(self.board["preys"])
        ]

        self.time_elapsed = 0
        self.hunter_moves = 0
        self.capture_order = []
        self.max_turns = 500
        self.movements = []
        self.frames = []
        self.save_frame()

    def alive_preys(self):
        return [
            prey
            for prey in self.preys
            if prey["alive"]
        ]

    def register_movement(
        self,
        entity_type,
        entity_number,
        from_position,
        to_position
    ):
        self.movements.append(
            {
                "entity_type": entity_type,
                "entity_number": entity_number,
                "from_x": from_position[0],
                "from_y": from_position[1],
                "to_x": to_position[0],
                "to_y": to_position[1],
                "turn": self.time_elapsed + 1,
            }
        )

    def save_frame(self):

        frame = {
            "turn": self.time_elapsed,
            "hunter": self.hunter,
            "preys": [
                {
                    "id": prey["id"],
                    "position": prey["position"],
                    "alive": prey["alive"]
                }
                for prey in self.preys
            ]
        }

        self.frames.append(frame)

    def capture_prey(self, prey):
        prey["alive"] = False
        prey["captured_at"] = self.time_elapsed + 1

        self.capture_order.append(prey["id"])

        print(
            f"CAPTURADA PRESA {prey['id']}"
        )

    def step(self):
        if self.time_elapsed >= self.max_turns:
            print("LIMITE DE TURNOS ALCANZADO")
            return False

        alive = self.alive_preys()

        if not alive:
            return False

        prey_positions = [
            prey["position"]
            for prey in alive
        ]

        old_hunter_position = self.hunter

        new_hunter_position = HunterAI.next_move(
            self.graph,
            self.hunter,
            prey_positions,
            self.hunter_algorithm
        )

        self.hunter = new_hunter_position
        self.hunter_moves += 1

        self.register_movement(
            "HUNTER",
            0,
            old_hunter_position,
            new_hunter_position
        )

        for prey in alive:
            if prey["position"] == self.hunter:
                self.capture_prey(prey)

        alive = self.alive_preys()

        if not alive:
            self.time_elapsed += 1
            return False

        occupied_positions = {
            prey["position"]
            for prey in alive
        }

        occupied_positions.add(self.hunter)

        for prey in alive:
            occupied_positions.remove(prey["position"])

            prey["history"].append(prey["position"])

            if len(prey["history"]) > 10:
                prey["history"].pop(0)

            old_prey_position = prey["position"]

            new_position = PreyAI.choose_move(
                self.graph,
                prey["position"],
                self.hunter,
                self.prey_algorithm,
                prey["history"]
            )

            if new_position not in occupied_positions:
                prey["position"] = new_position

            occupied_positions.add(prey["position"])

            prey["moves"] += 1
            prey["survival_time"] += 1

            self.register_movement(
                "PREY",
                prey["id"],
                old_prey_position,
                prey["position"]
            )

        for prey in self.alive_preys():
            if prey["position"] == self.hunter:
                self.capture_prey(prey)

        self.time_elapsed += 1
        self.save_frame()
        return True

    def print_board(self):
        size = self.board["size"]

        board = [
            ["." for _ in range(size)]
            for _ in range(size)
        ]

        for obstacle in self.board["obstacles"]:
            row, col = obstacle
            board[row][col] = "X"

        for prey in self.preys:
            if prey["alive"]:
                row, col = prey["position"]
                board[row][col] = str(prey["id"])

        row, col = self.hunter
        board[row][col] = "H"

        print()

        for row in board:
            print(" ".join(row))

        print()

    def ranking(self):
        return sorted(
            self.preys,
            key=lambda prey: (
                prey["captured_at"]
                if prey["captured_at"] is not None
                else 999999
            ),
            reverse=True
        )

    def print_ranking(self):
        print("\n" + "=" * 50)
        print("RANKING FINAL")
        print("=" * 50)

        for position, prey in enumerate(
            self.ranking(),
            start=1
        ):
            print(
                f"{position}. "
                f"Presa {prey['id']} | "
                f"Capturada en turno: "
                f"{prey['captured_at']} | "
                f"Movimientos: "
                f"{prey['moves']}"
            )

        print()
        print(f"Tiempo total: {self.time_elapsed}")
        print(f"Movimientos del cazador: {self.hunter_moves}")