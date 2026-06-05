from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):

    BOARD_SIZES = [
        (8, '8x8'),
        (10, '10x10'),
        (12, '12x12'),
        (15, '15x15'),
    ]

    ALGORITHMS = [
        ('DIJKSTRA', 'Dijkstra'),
        ('FLOYD', 'Floyd-Warshall'),
    ]

    STATUS = [
        ('WAITING', 'Esperando'),
        ('READY', 'Listo'),
        ('PLAYING', 'Jugando'),
        ('FINISHED', 'Finalizado'),
    ]

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=10,
        unique=True
    )

    board_size = models.IntegerField(
        choices=BOARD_SIZES,
        default=8
    )

    hunter_algorithm = models.CharField(
        max_length=20,
        choices=ALGORITHMS,
        default='DIJKSTRA'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='WAITING'
    )

    max_players = models.IntegerField(
        default=5
    )

    started = models.BooleanField(
        default=False
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def admin(self):
        return self.created_by

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class RoomParticipant(models.Model):

    ROLES = [
        ("HUNTER", "Cazador"),
        ("PREY_1", "Presa 1"),
        ("PREY_2", "Presa 2"),
        ("PREY_3", "Presa 3"),
        ("PREY_4", "Presa 4"),
    ]

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='participants'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default="PREY_1"
    )

    is_ready = models.BooleanField(
        default=False
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'room',
            'user'
        )

    def __str__(self):

        return (
            f"{self.user.username}"
            f" - "
            f"{self.role}"
        )