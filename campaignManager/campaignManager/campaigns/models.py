from django.db import models
from social.apps.django_app.default.models import UserSocialAuth
from campaignManager.armies.models import Army
  
# Create your models here.
class Campaign(models.Model):
    moderator   = models.ForeignKey(UserSocialAuth)
    armies      = models.ManyToManyField(Army)
    name        = models.CharField(max_length=128)
    blurb       = models.TextField(blank=True)
    turn        = models.CharField(max_length=64, default=1, blank=True)
    
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
      