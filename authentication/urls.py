from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    path('auth/register', RegistrationAPIView.as_view()),
    path('auth/login', LoginAPIView.as_view()),
    # single user view point to edit or update
    path('user/', UserRetrieveUpdateAPIView.as_view())
]