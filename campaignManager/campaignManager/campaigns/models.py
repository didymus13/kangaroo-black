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
    photo = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)
    
    def __unicode__(self):
        return self.name
    
    def is_owned_by(self, user):
        return self.moderator == user
    
    def is_participant(self, user):
        return user in self.participants.all()
    
    def _get_campaign_profiles(self):
        cps = []
        for p in self.participants.all():
            cps.append(p.campaignprofile_set.get(campaign=self))
        return cps
    campaign_profiles = property(_get_campaign_profiles)
    
class CampaignForm(ModelForm):
    from campaignManager.armies.models import Game
    class Meta:
        model = Campaign
        exclude = ['moderator', 'participants']
      