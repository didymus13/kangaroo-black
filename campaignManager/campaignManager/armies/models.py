from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from campaignManager.campaigns.models import Campaign

class Common(models.Model):
    name        = models.CharField(max_length=128)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name

class Game(Common):
    slug = models.SlugField(null=True)

class Faction(Common):
    game = models.ForeignKey(Game)
    slug = models.SlugField(null=True)
    
class Army(Common):
    user        = models.ForeignKey(User)
    faction     = models.ForeignKey(Faction, blank=True, null=True)
    campaign    = models.ForeignKey(Campaign, blank=True)
    blurb       = models.TextField(blank=True)
    armylist    = models.TextField(blank=True)
    public_list = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'armies'
        
    def is_owned_by(self, user):
        return self.user == user
        
class ArmyForm(ModelForm):
    class Meta:
        model = Army
        exclude = ['user']
