from django.urls import path

from .views import game_detail, generate_new_game, game_list


urlpatterns = [
    path("", game_list, name="game_list"),
    path("new/", generate_new_game, name="generate_new_game"),
    path("<int:game_id>/", game_detail, name="game_detail"),
]