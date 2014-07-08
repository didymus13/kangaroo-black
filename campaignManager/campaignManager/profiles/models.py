from django.db import models
from social.apps.django_app.default.models import UserSocialAuth
#from campaignManager.armies.models import Game
from django_countries.fields import CountryField
from django.forms import ModelForm

class Profile(models.Model):
    user = models.OneToOneField(UserSocialAuth)
    username = models.CharField(max_length=124, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    location = models.CharField(max_length=124, blank=True, null=True)
    country = CountryField(null=True, blank=True)
    games = models.ManyToManyField('armies.Game')
    bio = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.username

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'location', 'country', 'bio']
