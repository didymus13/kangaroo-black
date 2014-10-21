from django.test import TestCase
from campaignManager.turns.models import *
from campaignManager.campaigns.models import *
from django.contrib.auth.models import User
from campaignManager.armies.models import *
import uuid

# Create your tests here.
class TurnTestCase(TestCase):
    user = None
    tester = None
    turn = None
    
    def setUp(self):
        self.user = User.objects.create(username='MrUser', password='12345678')
        self.tester = User.objects.create(username='MrTester', password='12345678')
        game = Game.objects.create(name='test game system')
        campaign = Campaign.objects.create(moderator=self.user, game=game)
        self.turn = Turn.objects.create(campaign=campaign, label='initial turn')        
    
    """
    Feature: Only the current turn can be active
    Scenario: Create two turns in a campaign
    given active turn
    when active turn ends
    then active turn status becomes 'complete'
        and new turn status becomes 'active'
    """
    def test_only_one_active_turn_per_campaign(self):
        self.assertEqual(self.turn.status, self.turn.STATUS_ACTIVE)
        Turn.objects.create(campaign=self.turn.campaign, label='new turn');
        turns = self.turn.campaign.turn_set.all();
        
        self.assertEqual(1, turns.filter(status=Turn.STATUS_ACTIVE, label='new turn').count())
        self.assertEqual(1, turns.filter(status=Turn.STATUS_COMPLETE, label='initial turn').count())
    
    """
    Feature: Challenge expiration on turn end
    Scenario: End the current turn
    given current turn status active
        and one pending challenge
        and one accepted challenge
        and one completed challenge
    when current turn ends
    then all challenges have status complete
    """
    def test_turn_end_challenges_expire(self):
        self.assertEqual(Turn.STATUS_ACTIVE, self.turn.status)
        Challenge.objects.create(turn=self.turn, challenger=self.user, uuid=uuid.uuid4(),
            recipient=self.tester, status=Challenge.STATUS_PENDING )
        Challenge.objects.create(turn=self.turn, challenger=self.user, uuid=uuid.uuid4(), 
            recipient=self.tester, status=Challenge.STATUS_ACCEPTED )
        Challenge.objects.create(turn=self.turn, challenger=self.user, uuid=uuid.uuid4(), 
            recipient=self.tester, status=Challenge.STATUS_COMPLETE )
        
        Turn.objects.create(campaign=self.turn.campaign, label='new turn')
        
        challenges = self.turn.challenge_set.all()
        self.assertEqual(3, challenges.filter(status=Challenge.STATUS_COMPLETE).count())
        self.assertEqual(0, challenges.filter(status=Challenge.STATUS_ACCEPTED).count())
        self.assertEqual(0, challenges.filter(status=Challenge.STATUS_PENDING).count())