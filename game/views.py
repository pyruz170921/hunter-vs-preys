import random

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from ai.simulation import SimulationEngine
from game.services import SimulationPersistenceService
from lobby.models import Room

from .models import Game


def latest_game_detail(request):
    game = Game.objects.order_by("-id").first()

    if game is None:
        return render(request, "game/no_games.html")

    return redirect("game_detail", game_id=game.pk)


def generate_new_game(request):
    user = User.objects.first()

    hunter_algorithm = request.POST.get("hunter_algorithm", "DIJKSTRA")
    board_size = int(request.POST.get("board_size", 8))

    if hunter_algorithm not in ["DIJKSTRA", "FLOYD"]:
        hunter_algorithm = "DIJKSTRA"

    if board_size not in [8, 10, 12, 15]:
        board_size = 8

    room = Room.objects.create(
        name="Partida aleatoria",
        code=f"GAME{random.randint(10000, 99999)}",
        board_size=board_size,
        hunter_algorithm=hunter_algorithm,
        created_by=user,
    )

    simulation = SimulationEngine(board_size, hunter_algorithm)

    while simulation.step():
        pass

    game = SimulationPersistenceService.save_simulation(room, simulation)

    return redirect("game_detail", game_id=game.pk)


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    size = game.board.rows
    obstacles = list(game.board.obstacles.all().values("x", "y"))
    preys_queryset = game.preys.all().order_by("number")

    movements_data = list(
        game.movements.all()
        .order_by("turn", "id")
        .values(
            "turn",
            "entity_type",
            "entity_number",
            "from_x",
            "from_y",
            "to_x",
            "to_y",
        )
    )

    first_hunter_move = (
        game.movements
        .filter(entity_type="HUNTER")
        .order_by("turn", "id")
        .first()
    )

    initial_hunter = {
        "x": first_hunter_move.from_x if first_hunter_move else game.hunter.x,
        "y": first_hunter_move.from_y if first_hunter_move else game.hunter.y,
    }

    initial_preys = []

    for prey in preys_queryset:
        first_prey_move = (
            game.movements
            .filter(entity_type="PREY", entity_number=prey.number)
            .order_by("turn", "id")
            .first()
        )

        initial_preys.append({
            "number": prey.number,
            "x": first_prey_move.from_x if first_prey_move else prey.x,
            "y": first_prey_move.from_y if first_prey_move else prey.y,
            "alive": True,
        })

    context = {
        "game": game,
        "hunter": game.hunter,
        "preys": game.preys.all().order_by("ranking_position"),
        "movements": game.movements.all().order_by("turn"),
        "board_size": size,
        "obstacles": obstacles,
        "initial_hunter": initial_hunter,
        "initial_preys": initial_preys,
        "movements_data": movements_data,
    }

    return render(request, "game/detail.html", context)