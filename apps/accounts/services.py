from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        return user
