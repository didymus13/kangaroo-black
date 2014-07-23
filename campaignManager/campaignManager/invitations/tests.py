from django.test import TestCase, Client
from campaignManager.invitations.models import *
from django.contrib.auth.models import User
from campaignManager.campaigns.models import Campaign
from campaignManager.armies.models import Game
from django.core.urlresolvers import reverse
from django.core import mail
import uuid

# Create your tests here.
class InvitationTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        user = User.objects.create_user('mr_tester', 'test@example.com', '12345678')
        user.save()
        user = User.objects.create_user('mr_player', 'player@example.com', 'abcdef')
        game = Game(name='Test Game', slug='test-game')
        game.save()
        campaign = Campaign(name='test campaign', moderator=user, game=game)
        campaign.save()
    
    def test_send_invitation(self):
        campaign = Campaign.objects.get(name='test campaign')
        url = reverse('invitations:send', kwargs={'campaign_id':campaign.pk})
        self.c.login(username='mr_tester', password='12345678')
        
        response = self.c.get(url)
        self.assertContains(response, 'email')
        
        response = self.c.post(url, {'email':'player@example.com'}, follow=True)
        self.assertNotContains(response, 'Invitation not saved')
        self.assertNotContains(response, 'Invalid header detected')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Campaign Invitation')
        
        invitation = Invitation.objects.get(email='player@example.com')
        self.assertEqual(invitation.campaign, campaign, 'Campaigns do not match')
        self.assertEqual(invitation.email, 'player@example.com')
        
    def test_accept_invitation(self):
        uid = uuid.uuid4()
        campaign = Campaign.objects.get(name='test campaign')
        user = User.objects.get(email='player@example.com')
        invitation = Invitation(uuid=uid, campaign=campaign, email=user.email, user=user)
        invitation.save()
        
        url = reverse('invitations:accept', kwargs={'uuid':uid})
        self.c.login(username='mr_player', password='abcdef')
        response = self.c.get(url, kwargs={'uuid': uid}, follow=True)
        self.assertContains(response, campaign.name+' invitation accepted')
        
        