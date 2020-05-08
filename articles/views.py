from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer
from .renderers import ArticleJSONRenderer
# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'author__user')
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer, )
    lookup_field = 'slug'

    def create(self, request):
        serializer_context = {'author': request.user.profile}
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response(queryset)
