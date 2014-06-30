from django.db import models
from campaignManager.profiles.models import Profile

class Common(models.Model):
    name        = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        abstract = True

class Game(Common):
    pass

class Faction(Common):
    game = models.ForeignKey(Game)
    
class Army(Common):
    user        = models.ForeignKey(Profile)
    faction     = models.ForeignKey(Faction)
    blurb       = models.TextField(blank=True)
    armylist    = models.TextField(blank=True)
    public_list = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'armies'
