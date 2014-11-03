from django.shortcuts import render, get_object_or_404, redirect
from models import *
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from campaignManager.turns.models import Turn
from campaignManager.profiles.models import CampaignProfile

# Create your views here.
def detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    return render(request, 'detail.html', {
        'campaign': campaign,
        'user': request.user,
        'editable': campaign.is_owned_by(request.user),
        'is_participant': campaign.is_participant(request.user), 
        'header_image': campaign.photo,
    })

def index(request, status=None, slug=None):
    campaigns = Campaign.objects.all()
    if status: campaigns = campaigns.filter(status=status)
    if slug: campaigns = campaigns.filter(game__slug=slug)
    
    return render(request, 'index.html', {
        'campaigns': campaigns,
        'user': request.user,
    })
    
def looking_for_players(request):
    return index(request, Campaign.STATUS_LOOKING)

@login_required
def my_index(request):
    campaigns = Campaign.objects.filter(
        Q(moderator=request.user) | Q(participants=request.user)).distinct()
    return render(request, 'index.html', {
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
def dashboard(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    cp = CampaignProfile.objects.get(user=request.user, campaign=campaign)
    return render(request, 'dashboard.html', {
        'user': request.user,
        'cp': cp,
        'campaign': campaign,
        'editable': campaign.is_owned_by(request.user),
        'is_participant': campaign.is_participant(request.user),
        'page_title': 'Your ' + campaign.name + ' dashboard',
        'editable_profile': cp.user == request.user,
        'header_image': campaign.photo,
    })
