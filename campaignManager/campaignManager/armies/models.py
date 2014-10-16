from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from campaignManager.settings import UPLOAD_PATH

class ArmiesCommon(models.Model):
    name = models.CharField(max_length=128)
    name_short = models.CharField(max_length=5)
    photo = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)
    slug = models.SlugField(null=True)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name

class Game(ArmiesCommon):
    class Meta:
        ordering = ['name']

class Faction(ArmiesCommon):
    game = models.ForeignKey(Game)
    class Meta:
        ordering = ['game', 'name']
