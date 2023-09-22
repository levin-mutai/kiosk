from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer

from django.contrib.auth import login, authenticate

from oauth2_provider.models import AccessToken, Application
from .utils import generate_random_token
from django.utils import timezone


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # expiration_datetime = datetime.now() + timedelta(hours=8)
                expiration_datetime = timezone.now() + timezone.timedelta(hours=8)

                # Generate an OAuth2 access token
                try:
                    application = Application.objects.get(name="Kiosk")
                except Application.DoesNotExist:
                    application = Application.objects.create(
                        name="Test_app",
                        user=user,
                        client_type=Application.CLIENT_CONFIDENTIAL,
                        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
                        redirect_uris="http://localhost:8000/callback/",
                    )

                token = AccessToken.objects.create(
                    user=user,
                    application=application,  # Replace with your application instance
                    expires=expiration_datetime,
                    scope="openid",
                    token=generate_random_token(),
                )

                return Response(
                    {"access_token": token.token, "token_type": "Bearer"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
