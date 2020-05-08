import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """ Create and return a 'User' with an email, username and password."""

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password):
        """ Create and return a `User` with superuser (admin) permissions. """

        if password is None:
            raise TypeError('Superusers must have a super password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Each `User` needs a human-readable unique identifier that we can use to represent the `User` in the UI. We want to index this column in the database to improve lookup performance.
    """

    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(db_index=True, unique=True)
    # instead of deleting the user, offer to deactivate but keep data
    is_active = models.BooleanField(default=True)
    """The `is_staff` flag is expected by Django to determine who can and cannot log into the Django admin site. For most users this flag will always be false."""

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
     # More fields required by Django when specifying a custom user model.

     # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case it is set to be the EMAIL field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage objects of this type

    objects = UserManager()

    # representation of the Model

    def __str__(self):
        """ 
        Return a STRING - NOT JSON - representation of this User
        This string is used when a User is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Method that will allow to grab a user's token by calling `user.token`
        """
        return self._generate_jwt_token()

    def get_ful_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since there won't be the user's real name, return their username instead.
        """
        return self.username
    
    def get_short_name(self):

        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since there won't be the user's real name, return their username instead.
        """
        return self.username

    
    # CREATING THE TOKEN FOR THE USER

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry date set to 60 days into the future.

        Additional claims such as is_staff, username can be thrown in decode function of the model JWT
        """

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': f'{round(dt.timestamp())}',
            'username': self.username,
            'email': self.email,
            'admin': self.is_staff
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')