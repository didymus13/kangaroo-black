from django.db import models
from django.contrib.auth.models import User
from campaignManager.campaigns.models import Campaign
from django.forms import ModelForm
import uuid
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

# Create your models here.
class Invitation(models.Model):
    email = models.EmailField(max_length=254)
    campaign = models.ForeignKey(Campaign)
    uuid = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.uuid
    
    def send(self, request):
        self.uuid = uuid.uuid4()
        
        plaintext = get_template('email.txt')
        htmly = get_template('email.html')
        d = Context({'campaign': self.campaign, 'invitation': self, 'host': request.META['HTTP_HOST'] })
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        
        try:
            send_mail('Campaign Invitation', text_content, 
                self.campaign.moderator.email, [self.email,], 
                html_message=html_content)
        except:
            raise
        
        return True

class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ['user', 'uuid', 'campaign']
    