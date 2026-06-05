from django.test import TestCase
from django.contrib.auth.models import User

from lobby.models import (
    Room,
    RoomParticipant
)

from lobby.services import (
    GameStarter
)


class LobbyTest(TestCase):

    def test_room_can_start(self):

        admin = User.objects.create_user(
            username="admin"
        )

        room = Room.objects.create(
            name="Sala Test",
            code="TEST01",
            created_by=admin
        )

        RoomParticipant.objects.create(
            room=room,
            user=admin,
            role="HUNTER",
            is_ready=True
        )

        for i in range(1, 5):

            user = User.objects.create_user(
                username=f"user{i}"
            )

            RoomParticipant.objects.create(
                room=room,
                user=user,
                role=f"PREY_{i}",
                is_ready=True
            )

        game = GameStarter.start(room)

        self.assertIsNotNone(game)