import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class UniversalJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'

    def render(self, data, media_type=None, renderer_context=None):

        if isinstance(data, ReturnList):
            _data = json.loads(
                super(UniversalJSONRenderer, self).render(data).decode('utf-8')
            )
            return json.dumps({
                self.object_label_plural: _data
            })
        else:
            errors = data.get('errors', None)

            if errors is not None:
                return super(UniversalJSONRenderer, self).render(data)

            return json.dumps({
                self.object_label: data
            })
