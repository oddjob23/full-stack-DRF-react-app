from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Serializers registration requests and creates a new user """

    # make sure that password is at least 6 chars long and cannot be read by the client *write_only=True
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    # make token read only too so the cline cannot send a token along with a registration request

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # list of the fields that could be possibly included in the request or response
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # method that makes sure that current instacne of LoginSerializer is valid. Validates data that user provided and that combination of email and password matches

        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if email is not provided
        if email is None:
            raise serializers.ValidationError('An Email address is required to log in')
    
        # Raise an exception if a password is not provided

        if password is None:
            raise serializers.ValidationError('An Password address is required to log in')

        # user authenticate method from django
        # username = email because USERNAME_FIELD is set to email i UserModel (*field that is used to authenticate users)
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated')
    
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    """ Handle serialization and deserialization of a User objects."""

    # password must be at least 6 characters long but no more than 128
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', )

        read_only_fields = ('token', )
    
    def update(self, instance, validated_data):
        """ Performs update on a given User. """

        # Django has it's own function that handles hashing and salting passwords
        # Remove the password field from validated_data before iterating over it

        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, wset them on the current `USER` isntance one at a time.
            setattr(instance, key, value)
        
        if password is not None:
            # now user the django's function for hashing and salting password
            instance.set_password(password)
        
        instance.save()

        return instance # user