from django.db import models
from core.models import TimeStampModel
# Create your models here.
class Profile(TimeStampModel):

    # one-to-one relationship to authentication.User - Every user has one and only one profile!
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username