"""user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'user'
# Go to --> Authentication Views in django documentation

urlpatterns = [
    path("", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("profile/<int:id>/", views.profile, name="profile"),
    path('ip-check/', views.ip_check_view, name='ip-check'),
    path("password-change/", views.PasswordsChangeView.as_view(), name="password-change"),
    path("password-success/", views.password_success, name="password-success"),
]