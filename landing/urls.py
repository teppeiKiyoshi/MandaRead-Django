from django.http import request
from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from . import views

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

urlpatterns = [
    path('', CustomLoginView.as_view(template_name='landing/login.html', redirect_authenticated_user=True), name='landing-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing/logout.html'), name='landing-logout'),
    path('register/', views.register, name='landing-register')
]
