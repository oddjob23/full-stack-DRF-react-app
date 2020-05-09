
from django.urls import path, include
from .views import ArticleViewSet, CommentsListCreateAPIView, CommentDestoryAPIView, ArticleFavoriteAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('articles', ArticleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug:article_slug>/comments',
         CommentsListCreateAPIView.as_view()),
    path('articles/<slug:article_slug>/comments/<int:comment_pk>',
         CommentDestoryAPIView.as_view()),
    path('articles/<slug:article_slug>/favorite',
         ArticleFavoriteAPIView.as_view())
]
