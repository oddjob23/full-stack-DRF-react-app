import json

from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Received token is going to be type of bytes. Decode it before rendering the User object
        # If the view throws any sort an error, handle errors

        errors = data.get('errors', None)
        token = data.get('token', None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)
        
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')
        
        return json.dumps({
            'user': data
        })