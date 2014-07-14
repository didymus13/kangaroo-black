from django.db import models
from django.contrib.auth.models import User
from campaignManager.campaigns.models import Campaign

# Create your models here.
class Invitation(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField(max_length=254)
    campaign = models.ForeignKey(Campaign)
    uuid = models.CharField(max_length=254)
    
    def __unicode__(self):
        return self.identifier
    
    