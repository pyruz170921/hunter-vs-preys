from game.services import SimulationPersistenceService
from ai.simulation import SimulationEngine


class RoomValidator:

    REQUIRED_PLAYERS = 5

    @staticmethod
    def validate(room):

        participants = room.participants.all()

        if participants.count() != 5:
            raise Exception(
                "La sala debe tener exactamente 5 jugadores"
            )

        hunter_count = participants.filter(
            role="HUNTER"
        ).count()

        if hunter_count != 1:
            raise Exception(
                "Debe existir exactamente un cazador"
            )

        prey_count = participants.exclude(
            role="HUNTER"
        ).count()

        if prey_count != 4:
            raise Exception(
                "Debe existir exactamente cuatro presas"
            )

        if not all(
            p.is_ready
            for p in participants
        ):
            raise Exception(
                "Todos deben estar READY"
            )

        return True
    
class GameStarter:

    @staticmethod
    def start(room):

        RoomValidator.validate(room)

        simulation = SimulationEngine(
            room.board_size,
            room.hunter_algorithm
        )

        while simulation.step():
            pass

        game = (
            SimulationPersistenceService
            .save_simulation(
                room,
                simulation
            )
        )

        room.started = True
        room.status = "PLAYING"

        room.save()

        return game