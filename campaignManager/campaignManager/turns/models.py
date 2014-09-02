from django.db import models
from django.forms import ModelForm
import django.dispatch
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
import uuid
from django.template import Context

# Create your models here.
class Turn(models.Model):
    label = models.CharField(max_length=64, help_text='eg: Summer 1666, Stardate 12345.6')
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey('campaigns.Campaign', )
    
    def __unicode__(self):
        return self.label
    
    class Meta:
        ordering = ['-pk']

class TurnForm(ModelForm):
    class Meta:
        model = Turn
        exclude = ['campaign', 'created']