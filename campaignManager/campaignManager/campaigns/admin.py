from django.contrib import admin
from models import *
from campaignManager.armies.models import Army

admin.site.register(Campaign)
admin.site.register(CampaignArmy)
