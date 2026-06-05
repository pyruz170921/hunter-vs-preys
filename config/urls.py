from django.contrib import admin
from django.urls import path, include

from users.views import dashboard


urlpatterns = [

    path(
        "",
        dashboard,
        name="home"
    ),

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "users/",
        include("users.urls")
    ),

    path(
        "lobby/",
        include("lobby.urls")
    ),

    path(
        "games/",
        include("game.urls")
    ),
]