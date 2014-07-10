from django.shortcuts import render
from campaignManager.armies.models import *
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


# Create your views here.
def detail(request, pk):
    army = get_object_or_404(Army, pk=pk)
    return render_to_response('detail.html', {
        'request': request,
        'user': request.user,
        'army': army
    })

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
    context = RequestContext(request, {
        'request': request,
        'user': request.user
    })
    
    if pk: army = get_object_or_404(Army, pk=pk);
    
    if request.method == 'POST':
        if pk:
            form = ArmyForm(request.POST, instance=army)
        else:
            form = ArmyForm(request.POST)
        if form.is_valid():
            army = form.save(commit=False)
            army.user = request.user
            army.save()
            return redirect('armies:detail', pk=army.id)
        
    elif pk:
        form = ArmyForm(instance=army)
    else:
        form = ArmyForm()        
            
    return render_to_response('form.html', {
        'form': form,
        'request': request,
        'user': request.user,
    }, context_instance=context)
    
@login_required
def delete(request, pk):
    army = get_object_or_404(Army, pk=pk)
    army.delete()
    return redirect('armies:index')
