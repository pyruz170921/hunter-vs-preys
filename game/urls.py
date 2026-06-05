from django.urls import path

from .views import game_detail, generate_new_game

urlpatterns = [
    path(
        "new/",
        generate_new_game,
        name="generate_new_game"
    ),
    path(
        "<int:game_id>/",
        game_detail,
        name="game_detail"
    ),
]