from django.db import models
#from campaignManager.armies.models import Game
from django_countries.fields import CountryField
from django.forms import ModelForm
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=124, blank=True, null=True)
    country = CountryField(null=True, blank=True)
    games = models.ManyToManyField('armies.Game')
    bio = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.user
    
    def is_owned_by(self, user):
        print self.user == user
        return self.user == user

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'country', 'bio']
