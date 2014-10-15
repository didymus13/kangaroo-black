from django.contrib import admin
from models import *

# Register your models here.
class CommonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}

@admin.register(Faction)
class FactionAdmin(CommonAdmin):
    list_display = ('name', 'game')
    list_filter = ('game',)

class FactionTabular(admin.TabularInline):
    model = Faction
    
class GameAdmin(CommonAdmin):
    inlines = [FactionTabular,]
    
admin.site.register(Game, GameAdmin)