from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from .renderers import UserJSONRenderer

# Create your views here.

class RegistrationAPIView(APIView):
    # property which defines who can use this endpoint
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer, )
    def post(self, request):
        user = request.data.get('user', {})

        """ Create - Validate - Save pattern """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    renderer_classes = (UserJSONRenderer, )

    def post(self, request):
        user = request.data.get('user', {})

        # only need to validate data / method on the serializer

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, ) 
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer


    def retrieve(self, request, *args, **kwargs):
        # just serialize User object to JSON
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        # SERIALIZER - VALIDATE - SAVE pattern
        user_data = request.data.get('user', {})
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),

            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)