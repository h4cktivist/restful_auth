from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from uuid import uuid4

from .serializers import UserRegistrationSerializer, UserSerializer, TokenSerializer
from .utils import generate_access_token, generate_refresh_token


User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(User, email=serializer.data["email"])
        return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        serializer = TokenSerializer(data={
            "access_token": access_token,
            "refresh_token": refresh_token.token
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
