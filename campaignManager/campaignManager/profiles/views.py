from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext
from campaignManager.profiles.models import *
from django.contrib.auth.decorators import login_required

def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('home.html',
                             context_instance=context)

@login_required                             
def edit(request):
    profile = Profile.objects.get(user=request.user.id);
    form = ProfileForm(instance=profile)
    return render_to_response('form.html', {
        'request': request,
        'user': request.user,
        'form': form
    })
    
def detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    print profile;
    return render_to_response('detail.html', {
        'request': request,
        'profile': profile
    })
    