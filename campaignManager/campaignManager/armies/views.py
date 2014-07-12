from django.shortcuts import render
from campaignManager.armies.models import *
from django.shortcuts import render, render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

# Create your views here.
def detail(request, pk):
    army = get_object_or_404(Army, pk=pk, public_list=True)

    return render(request, 'detail.html', {
        'request': request,
        'user': request.user,
        'army': army,
        'editable': army.is_owned_by(request.user)
    })

def index(request, slug=None):
    if slug:
        armies = Army.objects.filter(faction__game__slug=slug, public_list=True)
    else:
        armies = Army.objects.filter(public_list=True)
    
    return render(request, 'index.html', {
        'request': request,
        'user': request.user,
        'armies': armies
    })
    
@login_required
def edit(request, pk=None):
    delete = None # Initial state
    
    if pk: 
        army = get_object_or_404(Army, pk=pk);
        if army.user and not army.is_owned_by(request.user):
            messages.add_message(
                request, 
                messages.ERROR, 
                'Armies can only be edited by their owners'
            )
            return redirect('armies:detail', pk=army.pk)
        delete = {'path': 'armies:delete', 'value': army.pk, }
            
    if request.method == 'POST':
        if pk:
            form = ArmyForm(request.POST, instance=army)
        else:
            form = ArmyForm(request.POST)
        if form.is_valid():
            army = form.save(commit=False)
            army.user = request.user
            army.save()
            messages.add_message(request, messages.SUCCESS, 'Save Successful' )
            
        return redirect('armies:detail', pk=army.pk)
        
    elif pk:
        form = ArmyForm(instance=army)
    else:
        form = ArmyForm()        
            
    return render(request, 'form.html', {
        'form': form,
        'request': request,
        'user': request.user,
        'delete': delete,
    })
    
@login_required
def delete(request, pk):
    army = get_object_or_404(Army, pk=pk)
    if army.is_owned_by(request.user):
        army.delete()
        messages.add_message(request, messages.SUCCESS, 'Delete successful')
        return redirect('armies:index')
    else:
        messages.add_message(request, messages.ERROR, 'Armies can only be deleted by their owners')
        return redirect('armies:detail', army.pk);
