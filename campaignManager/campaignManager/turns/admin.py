from django.contrib import admin
from webbrowser import register
from models import *

@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ('label', 'campaign')
    list_filter = ('campaign',)

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'challenger', 'recipient', 'turn')