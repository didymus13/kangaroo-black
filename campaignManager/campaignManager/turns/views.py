from django.shortcuts import render, get_object_or_404, redirect
from campaignManager.campaigns.models import Campaign
from campaignManager.turns.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid

# Create your views here.

@login_required    
def create(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    
    if not campaign.is_owned_by(request.user):
        messages.add_message(request, messages.WARNING, 'Only moderators can start this campaign')
        return redirect('campaigns:detail', campaign.pk)
    
    current_turn = None
    turns = campaign.turn_set.all()
    if turns:
        current_turn = turns[0]
    
    if request.method == 'POST':
        form = TurnForm(request.POST, request.FILES)
        if form.is_valid():
            if not current_turn:
                campaign.status = campaign.STATUS_PLAYING
                campaign.save()
            else:
                turn_finished.send(sender=current_turn.__class__, instance=current_turn)
            turn = form.save(commit=False)
            turn.campaign = campaign
            turn.save()
            return redirect('campaigns:detail', campaign.pk)
    else:
        form = TurnForm()
    
    return render(request, 'form.html', {
        'user': request.user,
        'form': form,
        'page_title': 'Create a new turn for ' + campaign.name
    })

@login_required
def edit(request, pk):
    turn = get_object_or_404(Turn, pk=pk)
    
    if not turn.campaign.is_owned_by(request.user):
        messages.add_message(request, messages.WARNING, 'Only moderators can edit turns')
        return redirect('campaigns:detail', campaign.pk)
    
    if request.method == 'POST':
        form = TurnForm(request.POST, request.FILES, instance=turn)
        if form.is_valid():
            form.save()
            return redirect('campaigns:detail', turn.campaign.pk)
    
    else:
        form = TurnForm(instance=turn)
    
    return render(request, 'form.html', {
        'user': request.user,
        'form': form,
        'page_title': 'editing turn:' + turn.label 
    })
    
@login_required
def challenge_send(request, pk, recipient):
    try:
        turn = Turn.objects.get(pk=pk)
        Challenge.objects.create(
            uuid=uuid.uuid4(), 
            turn = turn,
            challenger = request.user,
            recipient = User.objects.get(pk=recipient)
        )
        messages.add_message(request, messages.SUCCESS, 'Challenge issued!')
    except Exception as e:
        messages.add_message(request, messages.ERROR, 
            e)
    finally:
        return redirect('campaigns:detail', turn.campaign.pk)
    

@login_required
def challenge_accept(request, uuid):
    challenge = get_object_or_404(Challenge, uuid=uuid)
    try:
        challenge.accept(request.user)
        challenge.save()
        messages.add_message(request, messages.SUCCESS, 'Challenge accepted.')
    except:
        messages.add_message(request, messages.ERROR, 
            'An unknown error has occured. Challenge *not* accepted')
    finally:
        return redirect('campaigns:dashboard', challenge.turn.campaign.pk)
    
@login_required
def challenge_resolve(request, outcome, uuid):
    challenge = get_object_or_404(Challenge, uuid=uuid)
    try:
        challenge.resolve(outcome, request.user)
        messages.add_message(request, messages.SUCCESS, 
        'Challenge Resolved')
    except Exception as e:
        print e
        messages.add_message(request, messages.ERROR, e) 
    finally:
        return redirect('campaigns:dashboard', challenge.turn.campaign.pk)
