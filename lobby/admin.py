from django.contrib import admin
from .models import Room, RoomParticipant


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'code',
        'board_size',
        'hunter_algorithm',
        'status',
        'created_at'
    )


@admin.register(RoomParticipant)
class RoomParticipantAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'room',
        'user',
        'is_ready',
        'joined_at'
    )