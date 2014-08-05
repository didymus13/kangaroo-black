from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from campaignManager.settings import UPLOAD_PATH

class ArmiesCommon(models.Model):
    name = models.CharField(max_length=128)
    photo = models.FileField(blank=True, null=True, upload_to=UPLOAD_PATH)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name

class Game(ArmiesCommon):
    slug = models.SlugField(null=True)
    
    class Meta:
        ordering = ['name']

class Faction(ArmiesCommon):
    game = models.ForeignKey(Game)
    slug = models.SlugField(null=True)
    
class Army(ArmiesCommon):
    user = models.ForeignKey(User)
    faction = models.ForeignKey(Faction, blank=True, null=True)
    blurb = models.TextField(blank=True)
    armylist = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'armies'
        
    def is_owned_by(self, user):
        return self.user == user
        
class ArmyForm(ModelForm):
    class Meta:
        model = Army
        exclude = ['user']
