from django.db import models
from social.apps.django_app.default.models import UserSocialAuth

class Army(models.Model):
    user        = models.ForeignKey(UserSocialAuth)
    name        = models.CharField(max_length=128)
    faction     = models.CharField(max_length=128)
    blurb       = models.TextField(blank=True)
    armylist    = models.TextField(blank=True)
    public_list = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'armies'
