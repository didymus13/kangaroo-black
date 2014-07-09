from django.shortcuts import render
from campaignManager.armies.models import *
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


# Create your views here.
def detail(request):
    pass

def index(request, slug=None):
    if slug:
        armies = Army.objects.filter(faction__game__slug=slug, public_list=True)
    else:
        armies = Army.objects.all()
    
    return render_to_response('index.html', {
        'request': request,
        'user': request.user,
        'armies': armies
    })
    
@login_required
def edit(request, pk=None):
    pass
