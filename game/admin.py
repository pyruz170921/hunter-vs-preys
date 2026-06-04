from django.contrib import admin

from .models import (
    Game,
    Board,
    Obstacle,
    Hunter,
    Prey,
    Movement,
    GameEvent
)

admin.site.register(Game)
admin.site.register(Board)
admin.site.register(Obstacle)
admin.site.register(Hunter)
admin.site.register(Prey)
admin.site.register(Movement)
admin.site.register(GameEvent)