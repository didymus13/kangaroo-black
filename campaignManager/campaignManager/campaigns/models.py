from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from campaignManager.settings import UPLOAD_PATH
  
# Create your models here.
class Campaign(models.Model):
    STATUS_SETUP = 0
    STATUS_LOOKING = 100
    STATUS_PLAYING = 300
    STATUS_FINISHED = 500
    STATUS_HIATUS = 600
    
    CAMPAIGN_STATUS_FLAGS = (
        (STATUS_SETUP, 'setting up'),
        (STATUS_LOOKING, 'looking for players'),
        (STATUS_PLAYING, 'playing'),
        (STATUS_FINISHED, 'finished'),
        (STATUS_HIATUS, 'on hiatus'),
    )
    
    name = models.CharField(max_length=128)
    moderator = models.ForeignKey(User)
    game = models.ForeignKey('armies.Game')
    participants = models.ManyToManyField(
        User, 
        related_name='Participant', 
        blank=True)
    location = models.CharField(max_length=128, blank=True)
    country = CountryField(blank=True)
    online_only = models.BooleanField(default=False)
    blurb = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(
        default=STATUS_SETUP, 
        choices=CAMPAIGN_STATUS_FLAGS, )
    photo = models.FileField(blank=True, null=True, upload_to=UPLOAD_PATH)
    
    def __unicode__(self):
        return self.name
    
    def is_owned_by(self, user):
        return self.moderator == user
    
    def is_participant(self, user):
        return user in self.participants.all()
    
    def has_army(self, user):
        for campaignArmy in self.campaignarmy_set.all():
            if campaignArmy.army.user == user:
                return True
        return False
        
class CampaignForm(ModelForm):
    from campaignManager.armies.models import Game
    class Meta:
        model = Campaign
        exclude = ['moderator', 'participants']

class CampaignArmy(models.Model):
    army = models.OneToOneField('armies.Army')
    campaign = models.ForeignKey(Campaign)
    campaign_points = models.IntegerField(default=0)
    victory_points = models.IntegerField(default=0)
    currency = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.army.name
    
    def finish_game(self, cp=0, vp_for=0, vp_against=0, currency=0):
        self.campaign_points += cp
        self.victory_points += (vp_for - vp_against)
        self.currency += currency
    
    class Meta:
        ordering = ['-campaign_points', '-victory_points', '-currency', 'army']
        verbose_name_plural = 'campaign armies'
        
class CampaignArmyForm(ModelForm):
    class Meta:
        model = CampaignArmy
        exclude = ['campaign', 'campaign_points', 'victory_points', 'currency']
      