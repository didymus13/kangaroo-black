from django.contrib import admin
from models import *

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 
        'moderator', 
        'game', 
        'country', 
        'online_only', 
        'status', 
        'looking_for_players')
    list_filter = ('moderator', 'game', 'online_only', 'status', 'looking_for_players')