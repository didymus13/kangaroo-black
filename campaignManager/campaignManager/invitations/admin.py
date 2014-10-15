from django.contrib import admin
from models import *

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'created')
    list_filter = ('email', 'created')