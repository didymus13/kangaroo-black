from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import *
from campaignManager.profiles.models import CampaignProfile
import sys

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
        try:
            invitation = form.save(commit=False)
            invitation.campaign = campaign
            invitation.send(request)
            invitation.save()
            messages.add_message(request, messages.SUCCESS, 'Invitation sent')
        except:
            messages.add_message(request, messages.ERROR, 'Unexpected error:' + sys.exc_info())
        finally:
            return redirect('campaigns:detail', campaign.pk)
    
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