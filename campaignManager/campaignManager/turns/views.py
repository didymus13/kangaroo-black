from django.shortcuts import render, get_object_or_404, redirect
from campaignManager.campaigns.models import Campaign
from campaignManager.turns.models import TurnForm
from django.contrib import messages

# Create your views here.
def issue_challenge(request, turn_id, challenger_id, recipient_id):
    pass

    
def new_turn(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    
    if not campaign.is_owned_by(request.user):
        messages.add_message(request, errors.WARNING, 'Only moderators can start this campaign')
        return redirect('campaigns:detail', campaign.pk)
    
    current_turn = None
    turns = campaign.turn_set.all()
    if turns:
        current_turn = turns[:0].get()
    
    if request.method == 'POST':
        form = TurnForm(request.POST)
        if form.is_valid():
            if not current_turn:
                campaign.status = campaign.STATUS_PLAYING
                campaign.save()
            else:
                current_turn.finish()
                
            turn = form.save(commit=False)
            turn.campaign = campaign
            turn.save()
            return redirect('campaigns:detail', campaign.pk)
    else:
        form = TurnForm()
    
    return render(request, 'form.html', {
        'user': request.user,
        'form': form,
        'page_title': 'Create the first turn for ' + campaign.name
    })