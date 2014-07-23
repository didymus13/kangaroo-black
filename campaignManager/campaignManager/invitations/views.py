from django.shortcuts import render, redirect, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from models import *
from datetime import datetime, timedelta
import uuid

# Create your views here.
@login_required
def send_invitation(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    if not campaign.is_owned_by(request.user):
        messages.add_message(request, messages.WARNING, 
            'Invitations can only be made by the moderator')
        return redirect('campaigns:detail', campaign.pk)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            try: 
                user = User.objects.get(email=invitation.email)
            except User.DoesNotExist:
                user = None
                
            invitation.user = user
            invitation.uuid = uuid.uuid4()
            invitation.campaign = campaign
            invitation.save()
            
            plaintext = get_template('email.txt')
            htmly     = get_template('email.html')

            d = Context({'campaign': campaign, 'invitation': invitation, 'host': request.META['HTTP_HOST'] })

            subject, from_email, to = 'Campaign Invitations', campaign.moderator.email, invitation.email
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.add_message(request, messages.SUCCESS, 'Invitation sent')
            return redirect('campaigns:detail', campaign.pk)
        messages.add_message(request, messages.ERROR, 'Invitation not sent');
    
    form = InvitationForm()
    return render(request, 'form.html', {
        'user': request.user,
        'form': form, 
        'page_title': 'Invite participant'
    })

@login_required
def accept_invitation(request, uuid):
    invitation = get_object_or_404(Invitation, uuid=uuid)
    campaign = invitation.campaign
    try:
        campaign.participants.add(request.user)
        campaign.save()
        invitation.delete()
        messages.add_message(request, messages.SUCCESS, 
            campaign.name+' invitation accepted')
    except ValidationError:
        messages.add_message(request, messages.ERROR, 'Campaign validation error')
    except:
        messages.add_message(request, messages.ERROR, 
            'Invitation acceptance was not successful.')
    finally:
        return redirect('campaigns:detail', campaign.pk)