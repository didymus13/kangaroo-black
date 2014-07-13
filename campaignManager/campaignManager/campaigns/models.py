from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from campaignManager.armies.models import Army
from django_countries.fields import CountryField
  
# Create your models here.
class Campaign(models.Model):
    STATUS_SETUP = 0
    STATUS_LOOKING = 100
    STATUS_PLAYING = 300
    STATUS_FINISHED = 500
    
    CAMPAIGN_STATUS_FLAGS = (
        (STATUS_SETUP, 'setting up'),
        (STATUS_LOOKING, 'looking for players'),
        (STATUS_PLAYING, 'playing'),
        (STATUS_FINISHED, 'finished'),
    )
    
    moderator   = models.ForeignKey(User)
    armies      = models.ManyToManyField(Army)
    name        = models.CharField(max_length=128)
    location    = models.CharField(max_length=128, blank=True)
    country     = CountryField(blank=True)
    blurb       = models.TextField(blank=True)
    turn        = models.CharField(max_length=64, default=1, blank=True)
    status      = models.PositiveSmallIntegerField(
                    default=STATUS_SETUP, 
                    choices=CAMPAIGN_STATUS_FLAGS, )
    
    def __unicode__(self):
        return self.name

class CampaignMeta(models.Model):
    campaign    = models.ForeignKey(Campaign)
    label       = models.CharField(max_length=128)
    value       = models.CharField(max_length=254)
    
    def __unicode__(self):
        return self.label
    
    class Meta:
        verbose_name_plural = 'campaign meta'
        
class CampaignForm(ModelForm):
    model = Campaign
    exclude = ['moderator']
      