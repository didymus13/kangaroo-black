from django.db import models
from campaignManager.profiles.models import Profile

class Army(models.Model):
    user        = models.ForeignKey(Profile)
    name        = models.CharField(max_length=128)
    faction     = models.CharField(max_length=128)
    blurb       = models.TextField(blank=True)
    armylist    = models.TextField(blank=True)
    public_list = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'armies'
