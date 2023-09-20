from django.urls import path, include
from .views import UserRegistrationView, UserLoginView
from rest_framework.routers import DefaultRouter

login = DefaultRouter()
# login.register("/login", UserLoginViewSet, basename="user-login")


urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="user-registration"),
    path("login", UserLoginView.as_view(), name="login")
    # Define login endpoint if needed
]
