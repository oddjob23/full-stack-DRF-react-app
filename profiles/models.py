from django.db import models
from core.models import TimeStampModel
# Create your models here.


class Profile(TimeStampModel):

    # one-to-one relationship to authentication.User - Every user has one and only one profile!
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    following = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)

    favorites = models.ManyToManyField(
        'articles.Article', related_name='favorited_by')

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        # Folow profile if we are not already following a profile

        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def is_following(self, profile):
        # return true if following profile else returns false

        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, article):
        """ Favorite article if profile doesn't have it as favorite already"""
        self.favorites.add(article)

    def unfavorite(self, article):
        self.favorites.remove(article)

    def has_favorited(self, article):

        return self.favorites.filter(pk=article.pk).exists()
