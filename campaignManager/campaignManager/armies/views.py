from django.shortcuts import render
from campaignManager.armies.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from  django.http import HttpResponse

def get_game_factions(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return HttpResponse(serializers.serialize('json', game.faction_set.all()))