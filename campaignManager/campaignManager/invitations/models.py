from django.db import models
from django.contrib.auth.models import User
from campaignManager.campaigns.models import Campaign
from django.forms import ModelForm

# Create your models here.
class Invitation(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.EmailField(max_length=254)
    campaign = models.ForeignKey(Campaign)
    uuid = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.uuid

class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ['user', 'uuid', 'campaign']
    