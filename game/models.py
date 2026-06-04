from django.db import models
from lobby.models import Room


class Game(models.Model):

    STATUS_CHOICES = [
        ('WAITING', 'Esperando'),
        ('RUNNING', 'En ejecución'),
        ('FINISHED', 'Finalizada'),
    ]

    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE
    )

    seed = models.IntegerField()

    board_size = models.IntegerField()

    obstacle_count = models.IntegerField()

    start_time = models.DateTimeField(
        null=True,
        blank=True
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='WAITING'
    )

    def __str__(self):
        return f"Game {self.id}"
    

class Board(models.Model):

    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE
    )

    rows = models.IntegerField()

    columns = models.IntegerField()

    obstacle_percentage = models.FloatField(
        default=30.0
    )

    def __str__(self):
        return f"{self.rows}x{self.columns}"
    

class Obstacle(models.Model):

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='obstacles'
    )

    x = models.IntegerField()

    y = models.IntegerField()

    def __str__(self):
        return f"Obstacle ({self.x},{self.y})"


class Hunter(models.Model):

    ALGORITHMS = [
        ('DIJKSTRA', 'Dijkstra'),
        ('FLOYD', 'Floyd-Warshall'),
    ]

    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE
    )

    x = models.IntegerField()

    y = models.IntegerField()

    moves = models.IntegerField(
        default=0
    )

    algorithm = models.CharField(
        max_length=20,
        choices=ALGORITHMS
    )

    def __str__(self):
        return f"Hunter ({self.x},{self.y})"


class Prey(models.Model):

    ALGORITHMS = [
        ('DIJKSTRA', 'Dijkstra'),
        ('FLOYD', 'Floyd-Warshall'),
    ]

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='preys'
    )

    number = models.IntegerField()

    x = models.IntegerField()

    y = models.IntegerField()

    alive = models.BooleanField(
        default=True
    )

    moves = models.IntegerField(
        default=0
    )

    survival_time = models.FloatField(
        default=0
    )

    algorithm = models.CharField(
        max_length=20,
        choices=ALGORITHMS
    )

    def __str__(self):
        return f"Prey {self.number}"
    

class Movement(models.Model):

    ENTITY_TYPES = [
        ('HUNTER', 'Hunter'),
        ('PREY', 'Prey'),
    ]

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    entity_type = models.CharField(
        max_length=20,
        choices=ENTITY_TYPES
    )

    entity_number = models.IntegerField()

    from_x = models.IntegerField()

    from_y = models.IntegerField()

    to_x = models.IntegerField()

    to_y = models.IntegerField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )


class GameEvent(models.Model):

    EVENT_TYPES = [
        ('START', 'Inicio'),
        ('CAPTURE', 'Captura'),
        ('END', 'Fin'),
    ]

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    description = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )