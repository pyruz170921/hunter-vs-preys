import random
from game.models import Game
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from lobby.services import GameStarter

from .forms import RoomCreateForm
from .models import (
    Room,
    RoomParticipant
)


@login_required
def lobby_view(request):

    rooms = Room.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "lobby/lobby.html",
        {
            "rooms": rooms
        }
    )


@login_required
def my_room(request):

    participant = (
        RoomParticipant.objects
        .filter(
            user=request.user
        )
        .order_by("-id")
        .first()
    )

    if participant:

        return redirect(
            "room_detail",
            room_id=participant.room.id
        )

    return redirect(
        "lobby"
    )


@login_required
def create_room(request):

    existing_room = Room.objects.filter(
        created_by=request.user,
        started=False
    ).first()

    if existing_room:

        return redirect(
            "room_detail",
            room_id=existing_room.id
        )

    if request.method == "POST":

        form = RoomCreateForm(
            request.POST
        )

        if form.is_valid():

            room = form.save(
                commit=False
            )

            room.code = (
                f"ROOM{random.randint(1000,9999)}"
            )

            room.created_by = (
                request.user
            )

            room.save()

            RoomParticipant.objects.create(
                room=room,
                user=request.user,
                role="HUNTER"
            )

            return redirect(
                "room_detail",
                room_id=room.id
            )

    else:

        form = RoomCreateForm()

    return render(
        request,
        "lobby/create_room.html",
        {
            "form": form
        }
    )


@login_required
def room_detail(request, room_id):

    room = get_object_or_404(
        Room,
        pk=room_id
    )

    if room.started:

        game = room.game

        return redirect(
            "game_detail",
            game_id=game.id
        )

    participants = room.participants.all()

    return render(
        request,
        "lobby/room_detail.html",
        {
            "room": room,
            "participants": participants
        }
    )


@login_required
def join_room(request, room_id):

    room = get_object_or_404(
        Room,
        pk=room_id
    )

    if room.started:

        messages.error(
            request,
            "La partida ya inició."
        )

        return redirect(
            "lobby"
        )

    if RoomParticipant.objects.filter(
        room=room,
        user=request.user
    ).exists():

        return redirect(
            "room_detail",
            room_id=room.id
        )

    participants = (
        room.participants.count()
    )

    if participants >= 5:

        messages.error(
            request,
            "La sala está llena."
        )

        return redirect(
            "lobby"
        )

    roles = [
        "PREY_1",
        "PREY_2",
        "PREY_3",
        "PREY_4"
    ]

    used_roles = list(
        room.participants.values_list(
            "role",
            flat=True
        )
    )

    available_role = None

    for role in roles:

        if role not in used_roles:

            available_role = role
            break

    RoomParticipant.objects.create(
        room=room,
        user=request.user,
        role=available_role
    )

    return redirect(
        "room_detail",
        room_id=room.id
    )


@login_required
def toggle_ready(request, room_id):

    room = get_object_or_404(
        Room,
        pk=room_id
    )

    participant = get_object_or_404(
        RoomParticipant,
        room=room,
        user=request.user
    )

    participant.is_ready = (
        not participant.is_ready
    )

    participant.save()

    return redirect(
        "room_detail",
        room_id=room.id
    )


@login_required
def start_game(request, room_id):

    room = get_object_or_404(
        Room,
        pk=room_id
    )

    if request.user != room.admin:

        return redirect(
            "room_detail",
            room_id=room.id
        )

    existing_game = Game.objects.filter(
        room=room
    ).first()
    
    if existing_game:
    
        return redirect(
            "game_detail",
            game_id=existing_game.id
        )

    try:

        game = GameStarter.start(
            room
        )

    except Exception as error:

        print(error)

        messages.error(
            request,
            str(error)
        )

        return redirect(
            "room_detail",
            room_id=room.id
        )

    return redirect(
        "game_detail",
        game_id=game.id
    )