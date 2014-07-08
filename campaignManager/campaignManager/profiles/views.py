import profile
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template.context import RequestContext
from campaignManager.profiles.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('home.html',
                             context_instance=context)

@login_required                             
def edit(request):
    context = RequestContext(request, {
        'request': request,
        'user': request.user
    })
    user = User.objects.get(pk=request.user.id)
    profile, created = Profile.objects.get_or_create(user=user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:    
        form = ProfileForm(instance=profile)
        
    return render_to_response('form.html', {
        'request': request,
        'user': request.user,
        'form': form,
    }, context_instance=context)
    
def detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    print profile;
    return render_to_response('detail.html', {
        'request': request,
        'profile': profile,
        'user': request.user
    })
    