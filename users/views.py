from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import RefreshToken
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


class TokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token_uuid = request.data.get("refresh_token")

        if not refresh_token_uuid:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_uuid)
            if refresh_token.expires_at < timezone.now():
                refresh_token.delete()
                return Response({'error': 'Refresh token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except RefreshToken.DoesNotExist:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        user = refresh_token.user
        access_token = generate_access_token(user)
        new_refresh_token = generate_refresh_token(user)
        refresh_token.delete()

        serializer = TokenSerializer(data={
            "access_token": access_token,
            "refresh_token": new_refresh_token.token
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

        if refresh_token_obj.expires_at < timezone.now():
            return Response(
                {"error": "Refresh token has expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        refresh_token_obj.delete()

        return Response({"success": "User logged out."}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
