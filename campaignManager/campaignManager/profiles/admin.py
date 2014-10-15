from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Profile)

@admin.register(CampaignProfile)
class CampaignProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'cp', 'vp', 'win', 'tie', 'loss', 'matches')
    list_filter = ('campaign',)
