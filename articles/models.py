from django.db import models
from core.models import TimeStampModel
# Create your models here.


class Article(TimeStampModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()

    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title


class Comment(TimeStampModel):
    body = models.TextField()

    article = models.ForeignKey(
        'articles.Article', related_name='comments', on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )
