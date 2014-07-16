from django.shortcuts import render, redirect, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from models import *
from datetime import datetime, timedelta
import uuid

# Create your views here.
@login_required
def send_invitation(request, campaign_id):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        try:
            if form.is_valid():
                form.save(commit=False)
                invitation = form.save(commit=False)
                invitation.uuid = uuid.uuid4()
                invitation.campaign = Campaign.objects.get(pk=campaign_id)
                user = User.objects.get(email=invitation.email)
                invitation.user = user
                invitation.save()
                send_mail(
                    'Campaign Invitation', 
                    'You have been invited to a campagin',
                    request.user.email,
                    [invitation.email,],
                )
        except ValidationError:
            messages.add_message(request, messages.ERROR, 'Form submission invalid')
        except BadHeaderError:
            messages.add_message(request, messages.ERROR, 'Invalid email header detected')
            invitation.delete()
        finally:
            return redirect('campaigns:detail', campaign_id)
        
    
    form = InvitationForm()
    return render(request, 'form.html', {
        'user': request.user,
        'form': form
    })

@login_required
def accept_invitation(request, uuid):
    invitation = get_object_or_404(Invitation, user=request.user, uuid=uuid)
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