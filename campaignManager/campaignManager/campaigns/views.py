from django.shortcuts import render, get_object_or_404
from models import *
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    return render(request, 'campaigns_detail.html', {
        'campaign': campaign,
        'user': request.user,
        'editable': campaign.is_owned_by(request.user)
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
def edit(request, pk=None):
    pass

@login_required
def delete(request):
    pass
