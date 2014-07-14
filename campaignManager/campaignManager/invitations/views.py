from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import *

# Create your views here.
@login_required
def sendInvitation(request, campaign_id):
    if request.method == 'POST':
        pass # send invitation
    
    form = InvitationForm()
    return render(request, 'form.html', {
        'user': request.user,
        'form': form
    })

@login_required
def acceptInvitation(request, uuid):
    pass