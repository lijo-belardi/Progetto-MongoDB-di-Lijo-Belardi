from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# From this app
from .forms import NewUserForm
# Other apps import
from app.models import Wallet
# Other imports
import random


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_user = Wallet(
                user=user,
                btc_wallet=random.randrange(1, 11),
            )
            new_user.usd_wallet = new_user.btc_wallet * float(40000)
            new_user.save()
            login(request, user)
            messages.success(request, f"Registration successful. You recived {new_user.btc_wallet} bitcoin for the Registration." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="user/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("app:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("user:login")


@login_required()
def profile(request):
    return render(request, template_name="user/profile.html")


# Password change
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("user:password-success")


# Password success function
def password_success(request):
    return render(request, "registration/password_success.html", {})