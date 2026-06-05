from django.utils import timezone

from game.models import (
    Game,
    Board,
    Obstacle,
    Hunter,
    Prey,
    GameEvent,
    Movement,
    SimulationFrame,
)


class SimulationPersistenceService:

    @staticmethod
    def save_simulation(room, simulation):

        game = Game.objects.create(
            room=room,
            seed=0,
            board_size=simulation.board["size"],
            obstacle_count=len(simulation.board["obstacles"]),
            start_time=timezone.now(),
            end_time=timezone.now(),
            status="FINISHED",
            total_time=simulation.time_elapsed,
            hunter_moves=simulation.hunter_moves,
        )

        board = Board.objects.create(
            game=game,
            rows=simulation.board["size"],
            columns=simulation.board["size"],
            obstacle_percentage=30.0,
        )

        for obstacle in simulation.board["obstacles"]:
            Obstacle.objects.create(
                board=board,
                x=obstacle[0],
                y=obstacle[1],
            )

        Hunter.objects.create(
            game=game,
            x=simulation.hunter[0],
            y=simulation.hunter[1],
            moves=simulation.hunter_moves,
            algorithm=simulation.hunter_algorithm,
        )

        participants = {
            participant.role: participant.user
            for participant in room.participants.all()
        }
        
        for position, prey in enumerate(
            simulation.ranking(),
            start=1
        ):

            role_name = (
                f"PREY_{prey['id']}"
            )

            prey_user = (
                participants.get(role_name)
            )

            Prey.objects.create(
                game=game,
                number=prey["id"],
                user=prey_user,
                x=prey["position"][0],
                y=prey["position"][1],
                alive=prey["alive"],
                moves=prey["moves"],
                survival_time=prey["survival_time"],
                captured_at=prey["captured_at"],
                ranking_position=position,
                algorithm=simulation.prey_algorithm,
            )

        for movement in simulation.movements:
            Movement.objects.create(
                game=game,
                entity_type=movement["entity_type"],
                entity_number=movement["entity_number"],
                from_x=movement["from_x"],
                from_y=movement["from_y"],
                to_x=movement["to_x"],
                to_y=movement["to_y"],
                turn=movement["turn"],
            )

        for frame in simulation.frames:
            SimulationFrame.objects.create(
                game=game,
                turn=frame["turn"],
                state=frame,
            )

        GameEvent.objects.create(
            game=game,
            event_type="END",
            description="Simulación finalizada correctamente.",
            turn=simulation.time_elapsed,
        )

        return game