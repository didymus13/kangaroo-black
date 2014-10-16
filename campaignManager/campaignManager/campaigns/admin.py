from django.contrib import admin
from models import *

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'moderator', 'game', 'country', 'online_only', 'status')
    list_filter = ('moderator', 'game', 'online_only', 'status')