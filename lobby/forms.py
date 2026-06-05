from django import forms

from .models import Room


class RoomCreateForm(forms.ModelForm):

    class Meta:

        model = Room

        fields = [
            "name",
            "board_size",
            "hunter_algorithm"
        ]