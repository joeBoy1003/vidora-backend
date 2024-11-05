from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
import random
import string

User = get_user_model()  # Use the custom user model

def generate_random_name(email):
    username = email.split('@')[0]
    random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    random_name = username + '_' + random_string
    return random_name

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        password = request.data.get("password")
        email = request.data.get("email")

        if not password or not email:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = User.objects.create(
            username=generate_random_name(email),
            password=make_password(password),  # Securely hash the password
            email=email,
        )

        # Generate a token for the new user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
