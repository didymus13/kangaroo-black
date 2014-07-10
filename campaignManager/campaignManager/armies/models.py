from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Common(models.Model):
    name        = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        abstract = True

class Game(Common):
    slug = models.SlugField(null=True)

class Faction(Common):
    game = models.ForeignKey(Game)
    slug = models.SlugField(null=True)
    
class Army(Common):
    user        = models.ForeignKey(User)
    faction     = models.ForeignKey(Faction, blank=True, null=True)
    blurb       = models.TextField(blank=True)
    armylist    = models.TextField(blank=True)
    public_list = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'armies'
        
class ArmyForm(ModelForm):
    class Meta:
        model = Army
        exclude = ['user']
