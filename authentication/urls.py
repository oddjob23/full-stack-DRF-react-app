from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    path('auth/users/register', RegistrationAPIView.as_view()),
    path('auth/users/login', LoginAPIView.as_view()),
    # single user view point to edit or update
    path('auth/users/user', UserRetrieveUpdateAPIView.as_view())
]