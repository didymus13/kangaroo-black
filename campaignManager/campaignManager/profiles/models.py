from django.db import models
from social.apps.django_app.default.models import UserSocialAuth
#from campaignManager.armies.models import Game
from django_countries.fields import CountryField

class Profile(models.Model):
    user = models.OneToOneField(UserSocialAuth)
    username = models.CharField(max_length=124, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    location = models.CharField(max_length=124, blank=True, null=True)
    country = CountryField(null=True, blank=True)
    games = models.ManyToManyField('armies.Game')
    
    def __unicode__(self):
        return self.username