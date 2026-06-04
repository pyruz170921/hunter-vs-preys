from django.shortcuts import render, get_object_or_404, redirect

from .models import Game


def latest_game_detail(request):
    game = Game.objects.order_by("-id").first()

    if game is None:
        return render(request, "game/no_games.html")

    return redirect("game_detail", game_id=game.pk)


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    size = game.board.rows

    obstacles = list(
        game.board.obstacles.all().values("x", "y")
    )

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
            .filter(
                entity_type="PREY",
                entity_number=prey.number
            )
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
        "events": game.events.all().order_by("turn"),
        "movements": game.movements.all().order_by("turn"),
        "board_size": size,
        "obstacles": obstacles,
        "initial_hunter": initial_hunter,
        "initial_preys": initial_preys,
        "movements_data": movements_data,
    }

    return render(request, "game/detail.html", context)