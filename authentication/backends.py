import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
                This method is called on EVERY request!
                authenticate - has two possible return values:
                    1) `None` - If you want to refuse the request, return None. 
                            - Example: Request header does not include Token
                    2) `(user, token)` - If there is a valid token return user/token combination when authentication is successful

                                        - If something else is the case raise the AuthenticationFailed exception 
        """

        request.user = None

        """
            `auth_header` is the array with two elements: 1 - the name of the authentication header ( TOKEN ) 
                                                        2 - the JWT ( value of the TOKEN)
                                                
        """
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower() # this should return "token"

        if not auth_header:
           return None

        if len(auth_header) == 1:
            # this is invalid authorization header 

            return None
        elif len(auth_header) > 2:
            # again invalid header
            return None
        
        # decode prefix and JWT

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):

        """
            Try to authenticate the given credentials. If authentication is successful, return user and token, if not throw THE ERROR AT MADAFAKA
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found'
            raise exceptions.AuthenticationFailed(msg)
    
        if not user.is_active:
            msg = "This user has been deactivated"
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)