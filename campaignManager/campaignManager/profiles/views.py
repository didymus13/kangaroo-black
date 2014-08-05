from django.shortcuts import render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template.context import RequestContext
from campaignManager.profiles.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from campaignManager.armies.models import *
from campaignManager.campaigns.models import *

def home(request):
   return render(request, 'home.html')

@login_required                             
def edit(request, username):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if not created and profile.user != user:
        messages.add_message(request, message.WARNING, 'User can only edit their own profile')
        return redirect('profiles:detail', request.user.username)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile:detail', username=user.username)
        
    form = ProfileForm(instance=profile)
        
    return render(request, 'form.html', {
        'user': request.user,
        'form': form,
        'page_title': user
    })
    
def detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    armies = Army.objects.filter(user=user)
    campaigns = Campaign.objects.filter(participants=user)
    my_campaigns = Campaign.objects.filter(moderator=user)
    return render(request, 'profiles_detail.html', {
        'request': request,
        'profile': profile,
        'user': request.user,
        'armies': armies,
        'campaigns': campaigns,
        'my_campaigns': my_campaigns,
        'editable': profile.is_owned_by(request.user)
    })
    