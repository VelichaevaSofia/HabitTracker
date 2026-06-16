from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


class AuthService:
    
    @staticmethod
    def register_user(form):
        user = form.save()
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        return user
    
    @staticmethod
    def login_user(request, user):
        login(request, user)
    
    @staticmethod
    def logout_user(request):
        logout(request)