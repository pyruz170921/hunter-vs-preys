from django.contrib import admin

from .models import (
    Game,
    Board,
    Obstacle,
    Hunter,
    Prey,
    Movement,
    GameEvent,
)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room",
        "board_size",
        "status",
        "total_time",
        "hunter_moves",
        "start_time",
        "end_time",
    )

    list_filter = (
        "status",
        "board_size",
    )

    search_fields = (
        "room__name",
        "room__code",
    )


@admin.register(Prey)
class PreyAdmin(admin.ModelAdmin):
    list_display = (
        "game",
        "number",
        "alive",
        "moves",
        "survival_time",
        "captured_at",
        "ranking_position",
        "algorithm",
    )

    list_filter = (
        "alive",
        "algorithm",
        "ranking_position",
    )


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = (
        "game",
        "turn",
        "entity_type",
        "entity_number",
        "from_x",
        "from_y",
        "to_x",
        "to_y",
    )

    list_filter = (
        "entity_type",
        "turn",
    )


admin.site.register(Board)
admin.site.register(Obstacle)
admin.site.register(Hunter)
admin.site.register(GameEvent)