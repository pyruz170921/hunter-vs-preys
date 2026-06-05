from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import (
    login_required
)

from django.contrib.auth.models import User

from django.shortcuts import (
    render,
    redirect
)

from .forms import RegisterForm
from .models import Profile


def register_view(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            Profile.objects.create(
                user=user,
                nickname=form.cleaned_data["nickname"]
            )

            login(
                request,
                user
            )

            return redirect(
                "dashboard"
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            return redirect(
                "dashboard"
            )

        error = (
            "Credenciales inválidas"
        )

    return render(
        request,
        "users/login.html",
        {
            "error": error
        }
    )


def logout_view(request):

    logout(request)

    return redirect(
        "login"
    )


@login_required
def dashboard(request):

    return render(
        request,
        "users/dashboard.html",
        {
            "profile": request.user.profile
        }
    )


@login_required
def profile_view(request):

    return render(
        request,
        "users/profile.html",
        {
            "profile": request.user.profile
        }
    )