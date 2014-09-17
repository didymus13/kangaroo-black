from django.db import models
#from campaignManager.armies.models import Game
from django_countries.fields import CountryField
from django.forms import ModelForm
from django.contrib.auth.models import User
from campaignManager.settings import UPLOAD_PATH

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=124, blank=True, null=True)
    country = CountryField(null=True, blank=True)
    games = models.ManyToManyField('armies.Game')
    bio = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)
    
    def __unicode__(self):
        return self.user.username
    
    def is_owned_by(self, user):
        print self.user == user
        return self.user == user

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]
        
class CampaignProfile(models.Model):
    """ 
    Each user can have a multiple campaign standings. Campaign points and
    Victory points and currency are essentially placeholders for two types of 
    rankings. Campaign points are the stronger of the three. The others are 
    tiebreakers
    """
    STATUS_WIN = 2
    STATUS_TIE = 1
    STATUS_LOSS = 0
    OUTCOMES = {
        'win': STATUS_WIN,
        'tie': STATUS_TIE,
        'loss': STATUS_LOSS
    }
    
    user = models.ForeignKey(User)
    campaign = models.ForeignKey('campaigns.Campaign')
    # Campaign Points 
    cp = models.IntegerField(default=0)
    # Victory Points 
    vp = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    tie = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-cp', '-vp',]
    
    def __unicode__(self):
        return self.user.username
    
    def _get_matches(self):
        return self.win + self.tie + self.loss
    matches = property(_get_matches)
    
    def calc_outcome(self, status, vp):
        """ Calculates the various stats relative to performance """
        if status == 'win':
            self.win += 1
        elif status == 'tie':
            self.tie += 1
        elif status == 'loss':
            self.loss += 1
        
        self.cp += OUTCOMES[status]
        self.vp += vp
    
    
