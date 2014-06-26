from django.db import models
from social.apps.django_app.default.models import UserSocialAuth

class Profile(models.Model):
    user = models.ForeignKey(UserSocialAuth)
    username = models.CharField(max_length=124)
    
    def __unicode__(self):
        return self.username