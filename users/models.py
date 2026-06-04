from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    COLORS = [
        ('red', 'Rojo'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
        ('yellow', 'Amarillo'),
        ('purple', 'Morado'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    nickname = models.CharField(
        max_length=50,
        unique=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=20,
        choices=COLORS,
        default='blue'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nickname
