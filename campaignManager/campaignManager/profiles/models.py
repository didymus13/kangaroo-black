from django.db import models
from django_countries.fields import CountryField
from django.forms import ModelForm
from django.contrib.auth.models import User
from campaignManager.settings import UPLOAD_PATH
from campaignManager.turns.models import Challenge
from django.db.models.signals import post_save
from django.dispatch import receiver
from campaignManager.campaigns.models import Campaign
from campaignManager.turns.models import Challenge, challenge_complete

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=124, blank=True, null=True)
    country = CountryField(null=True, blank=True)
    games = models.ManyToManyField('armies.Game')
    bio = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)
    
    def __unicode__(self):
        return self.user.username
    
    def is_owned_by(self, user):
        print self.user == user
        return self.user == user

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=kwargs.get('instance'));

    
class CampaignProfile(models.Model):
    """ 
    Each user can have a multiple campaign standings. Campaign points and
    Victory points and currency are essentially placeholders for two types of 
    rankings. Campaign points are the stronger of the three. The others are 
    tiebreakers
    """
    STATUS_WIN = 2
    STATUS_TIE = 1
    STATUS_LOSS = 0
    OUTCOMES = {
        'win': STATUS_WIN,
        'tie': STATUS_TIE,
        'loss': STATUS_LOSS
    }
    
    user = models.ForeignKey(User)
    faction = models.ForeignKey('armies.Faction', blank=True, null=True)
    campaign = models.ForeignKey('campaigns.Campaign')
    # Campaign Points 
    cp = models.IntegerField(default=0)
    # Victory Points 
    vp = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    tie = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-cp', '-vp',]
    
    def __unicode__(self):
        return self.user.username
    
    def _get_matches(self):
        return self.win + self.tie + self.loss
    matches = property(_get_matches)
    
    def _get_challenges_sent(self):
        return self.user.challenger.all()
    challenges_sent = property(_get_challenges_sent)
    
    def _get_challenges_recieved(self):
        return self.user.recipient.all()
    challenges_received = property(_get_challenges_recieved)
    
    def _get_challenges_won(self):
        return self.user.winner.all()
    challenges_won = property(_get_challenges_won)
        
    def calc_outcome(self, status, vp):
        """ Calculates the various stats relative to performance """
        if status == 'win':
            self.win += 1
        elif status == 'tie':
            self.tie += 1
        elif status == 'loss':
            self.loss += 1
        
        self.cp += self.OUTCOMES[status]
        self.vp += vp

@receiver(post_save, sender=Campaign)
def ensure_campaign_profiles_exist(sender, **kwargs):
    campaign = kwargs.get('instance')
    for participant in campaign.participants.all():
        CampaignProfile.objects.get_or_create(campaign=campaign, user=participant)

@receiver(challenge_complete, sender=Challenge)
def process_outcome(sender, **kwargs):
    challenge = kwargs.get('instance')
    
    winner = CampaignProfile.objects.get(
        campaign=challenge.turn.campaign, 
        user=challenge.winner
    )
    loser = CampaignProfile.objects.get(
        campaign=challenge.turn.campaign, 
        user=challenge.loser
    )
    if winner and loser: 
        winner.calc_outcome('win', 0)
        winner.save()
        loser.calc_outcome('loss', 0)
        loser.save()