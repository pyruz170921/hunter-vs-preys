from django.urls import path

from .views import (
    lobby_view,
    create_room,
    room_detail,
    join_room,
    toggle_ready,
    start_game,
    my_room
)

urlpatterns = [

    path(
        "",
        lobby_view,
        name="lobby"
    ),

    path(
        "my-room/",
        my_room,
        name="my_room"
    ),

    path(
        "create/",
        create_room,
        name="create_room"
    ),

    path(
        "<int:room_id>/",
        room_detail,
        name="room_detail"
    ),

    path(
        "<int:room_id>/join/",
        join_room,
        name="join_room"
    ),

    path(
        "<int:room_id>/ready/",
        toggle_ready,
        name="toggle_ready"
    ),

    path(
        "<int:room_id>/start/",
        start_game,
        name="start_game"
    ),
]