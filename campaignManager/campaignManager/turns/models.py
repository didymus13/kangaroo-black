from django.db import models
from django.forms import ModelForm
from django.core.mail import send_mail
import uuid
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User

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
        
class Challenge(models.Model):
    STATUS_PENDING = 0
    STATUS_ACCEPTED = 10
    STATUS_COMPLETE = 100
    STATUS_CHOICES = [
        ['pending', STATUS_PENDING], 
        ['accepted', STATUS_ACCEPTED], 
        ['complete', STATUS_COMPLETE]
    ]
    
    turn = models.ForeignKey(Turn)
    uuid = models.CharField(max_length=254)
    challenger = models.ForeignKey(User, related_name='challenger')
    recipient = models.ForeignKey(
        User, 
        related_name='recipient', 
        blank=True, 
        null=True
    )
    winner = models.ForeignKey(User, blank=True, null=True, related_name='winner')
    issued_date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    class Meta:
        ordering = ['-turn', '-issued_date']
    
    def __unicode__(self):
        return self.uuid
    
    def send(self):
        subject = 'You have been challenged!'
        content = 'You have been challenged by ' + self.challenger + ' from the ' + self.turn.campaign + ' campaign.'
        send_mail(subject, content, self.challenger.email, [self.recipient.email,])
    
    def accept(self, user):
        if user == self.recipient and self.status == STATUS_PENDING:
            self.status = STATUS_ACCEPTED
            self.save()
            return True
        else:
            raise Exception('An unkown error occured: Challenge *not* accepted')
    
    def complete(self, winner, loser):
        if self.is_participant(winner) and self.is_participant(loser):
            self.winner = winner
            self.status = STATUS_COMPLETE
            # @TODO: SEND WINNER AND LOSER SIGNALS
            return self.save()
        else:
            return false
    
    def is_participant(self, user):
        if self.user in [self.challenger, self.recipient]:
            return True
        return false

class ResultForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ['winner',]