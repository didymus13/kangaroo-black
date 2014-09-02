from django.shortcuts import render, get_object_or_404, redirect
from models import *
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from campaignManager.turns.models import Turn

# Create your views here.
def detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    user_army = CampaignArmy.objects.filter(
            army__user=request.user.id, campaign=campaign)
    
    return render(request, 'campaigns_detail.html', {
        'campaign': campaign,
        'user': request.user,
        'editable': campaign.is_owned_by(request.user),
        'user_army': user_army,
        'is_participant': campaign.is_participant(request.user),
        'has_army': campaign.has_army(request.user), 
    })

def index(request, status=None, slug=None):
    campaigns = Campaign.objects.all()
    if status: campaigns = campaigns.filter(status=status)
    if slug: campaigns = campaigns.filter(game__slug=slug)
    
    return render(request, 'campaigns_index.html', {
        'campaigns': campaigns,
        'user': request.user,
    })

@login_required
def my_index(request):
    campaigns = Campaign.objects.filter(Q(moderator=request.user) | Q(participants=request.user)) 
    print campaigns
    return render(request, 'campaigns_index.html', {
        'campaigns': campaigns,
        'user': request.user
    })

@login_required
def edit(request, pk=None):
    delete = None # Initial state
    
    if pk: 
        campaign = get_object_or_404(Campaign, pk=pk);
        if campaign.moderator and not campaign.is_owned_by(request.user):
            messages.add_message(
                request, 
                messages.ERROR, 
                'Campaigns can only be edited by their owners'
            )
            return redirect('campaigns:detail', pk=campaign.pk)
        delete = {'path': 'campaigns:delete', 'value': campaign.pk, }
            
    if request.method == 'POST':
        if pk:
            form = CampaignForm(request.POST, request.FILES, instance=campaign)
        else:
            form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.moderator = request.user
            campaign.save()
            messages.add_message(request, messages.SUCCESS, 'Save Successful' )
            
        return redirect('campaigns:detail', pk=campaign.pk)
        
    elif pk:
        form = CampaignForm(instance=campaign)
    else:
        form = CampaignForm()        
            
    return render(request, 'form.html', {
        'form': form,
        'user': request.user,
        'delete': delete,
        'page_title': 'Edit Campaign',
    })

@login_required
def delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if campaign.is_owned_by(request.user):
        campaign.delete()
        messages.add_message(request, messages.SUCCESS, 'Delete successful')
        return redirect('campaigns:index')
    else:
        messages.add_message(request, messages.ERROR, 
                'Campaigns can only be deleted by their owners')
        return redirect('campaigns:detail', campaign.pk)

@login_required
def new_campaign_army(request, pk):
    
    from campaignManager.armies.models import ArmyForm
    
    campaign = get_object_or_404(Campaign, pk=pk)
    
    if not campaign.is_participant(request.user):
        messages.add_message(request, messages.WARNING, 
                'Only campaign participants can create armies')
        return redirect('campaign:detail', pk)
    
    if request.method == 'POST':
        form = ArmyForm(request.POST, request.FILES)
        if form.is_valid():
            army = form.save(commit=False)
            army.user = request.user
            army.save()
            campaign_army = CampaignArmy.objects.create(
                army=army, 
                campaign=campaign)
            campaign_army.save()
            return redirect('armies:detail', army.pk)
    
    else:
        form = ArmyForm()
    
    return render(request, 'form.html', {
        'user': request.user,
        'form': form,
        'page_title': 'Create a new Campaign Army'
    })
    
def standings(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    turns = campaign.turn_set.all()
    current_turn = False
    if turns:
        current_turn = turns[:0]
    
    return render(request, 'campaigns_standings.html', {
        'user': request.user,
        'campaign': campaign,
        'page_title': campaign.name + ' standings',
        'editable': campaign.is_owned_by(request.user),
        'is_participant': campaign.is_participant(request.user),
        'current_turn': current_turn,
    })
