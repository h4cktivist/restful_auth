from django.urls import path
from .views import UserRegistrationView, UserLoginView,\
    TokenRefreshView, UserLogoutView, UserProfileView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='me'),
]
