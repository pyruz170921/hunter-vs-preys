from django import forms
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    nickname = forms.CharField(
        max_length=50
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "password"
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password != confirm_password:

            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        return cleaned_data