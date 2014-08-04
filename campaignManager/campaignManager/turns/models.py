from django.db import models
from django.forms import ModelForm
import django.dispatch

# Create your models here.
class Turn(models.Model):
    label = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey('campaigns.Campaign')
    
    def __unicode__(self):
        return label
    
    class Meta:
        ordering = ['-pk']

class TurnForm(ModelForm):
    class Meta:
        model = Turn
        fields = ['label', ]
        
class Challenge(models.Model):
    PENDING = 10
    COMPLETE = 100
    STATUS = ((PENDING, 'pending'), (COMPLETE, 'complete'))
    
    turn = models.ForeignKey(Turn)
    participants = models.ManyToManyField('campaigns.CampaignArmy')
    winner = models.ForeignKey('campaigns.CampaignArmy', blank=True, related_name='winner')
    status = models.PositiveIntegerField(choices=STATUS)
