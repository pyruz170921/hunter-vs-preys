from django.urls import path

from .views import game_detail

urlpatterns = [
    path(
        "<int:game_id>/",
        game_detail,
        name="game_detail"
    ),
]
