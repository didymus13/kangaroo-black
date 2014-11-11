from django.db import models
from django.forms import ModelForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.dispatch import receiver
import django.dispatch
from django.db.models.signals import post_save
from campaignManager.settings import UPLOAD_PATH
from PIL import Image
import os

# Create your models here.
class Turn(models.Model):
    STATUS_PENDING = 0
    STATUS_ACTIVE = 50
    STATUS_COMPLETE = 100
    STATUS_CHOICES = [
        [STATUS_PENDING, 'initial'],
        [STATUS_ACTIVE, 'active'],
        [STATUS_COMPLETE, 'complete']
    ]
    label = models.CharField(max_length=64, help_text='eg: Summer 1666, Stardate 12345.6')
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey('campaigns.Campaign', )
    status = models.PositiveIntegerField(default=STATUS_PENDING, choices=STATUS_CHOICES)
    _map = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)
    map_thumbnail = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)

    def set_map(self, val):
        self._map = val
        self._map_changed = True

    def get_map(self):
        return self._map

    map = property(get_map, set_map)

    def save(self, *args, **kwargs):
        super(Turn, self).save(*args, **kwargs)
        
        if getattr(self, '_map_changed', True):
            try:
                map = Image.open(self.map)
                map.load()
                map.thumbnail((500, 500), Image.ANTIALIAS)
                map.save(self.map.path)
                print self.map.path
            except Exception as ex:
                print 'Error: %s' % ex

    def __unicode__(self):
        return self.label
    
    class Meta:
        ordering = ['-pk']

class TurnForm(ModelForm):
    class Meta:
        model = Turn
        exclude = ['campaign', 'created', 'status', 'map_thumbnail']

turn_finished = django.dispatch.Signal(providing_args=['instance',])

@receiver(post_save, sender=Turn)
def expire_old_turns(sender, **kwargs):
    if kwargs.get('created', False):
        turn = kwargs.get('instance')
        
        for t in turn.campaign.turn_set.all():
            if t.status != t.STATUS_COMPLETE:
                t.status = t.STATUS_COMPLETE
                t.save()
                turn_finished.send(sender=t.__class__, instance=t)
        
        turn.status = turn.STATUS_ACTIVE
        turn.save()
        
class Challenge(models.Model):
    STATUS_PENDING = 0
    STATUS_ACCEPTED = 10
    STATUS_COMPLETE = 100
    STATUS_CHOICES = [
        [STATUS_PENDING, 'pending'], 
        [STATUS_ACCEPTED, 'accepted'], 
        [STATUS_COMPLETE, 'complete']
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
    
    
    def _get_loser(self):
        if not self.winner:
            return false
        elif self.winner == self.challenger:
            return self.recipient
        return self.challenger
    loser = property(_get_loser)
    
    class Meta:
        ordering = ['-issued_date', '-turn']
    
    def __unicode__(self):
        return self.uuid
    
    def send(self):
        subject = 'You have been challenged!'
        content = 'You have been challenged by ' + self.challenger + ' from the ' + self.turn.campaign + ' campaign.'
        send_mail(subject, content, self.challenger.email, [self.recipient.email,])
    
    def accept(self, user):
        if user == self.recipient and self.status == self.STATUS_PENDING:
            self.status = self.STATUS_ACCEPTED
        else:
            raise Exception('An unkown error occured: Challenge *not* accepted')

    def _get_win_participants(self, user):
        if self.challenger == user:
            return { 'winner': self.challenger, 'loser': self.recipient }
        else:
            return { 'winner': self.recipient, 'loser': self.challenger }
    
    def _get_loss_participants(self, user):
        if self.challenger == user:
            return { 'winner': self.recipient, 'loser': self.challenger }
        else:
            return { 'winner': self.challenger, 'loser': self.recipient }
    
    def resolve(self, outcome, user):
        if (outcome == 'win'):
            results = self._get_win_participants(user)
        elif (outcome == 'loss'):
            results = self._get_loss_participants(user)
        elif (outcome == 'tie'):
            pass
        else:
            raise Exception('Invalid outcome: must be "win", "tie", or "loss"')
        
        self.winner = results['winner']
        self.status = self.STATUS_COMPLETE
        challenge_complete.send(sender=self.__class__, instance=self)
        self.save()
    
    def is_participant(self, user):
        if self.user in [self.challenger, self.recipient]:
            return True
        return false

class ResultForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ['winner',]

challenge_complete = django.dispatch.Signal(providing_args=['instance',])

@receiver(turn_finished, sender=Turn)
def force_resolve_challenges(sender, **kwargs):
    challenges = kwargs.get('instance').challenge_set.all()
    for challenge in challenges:
        challenge.status = Challenge.STATUS_COMPLETE
        challenge.save()
