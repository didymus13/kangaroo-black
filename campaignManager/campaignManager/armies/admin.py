from django.contrib import admin
from models import *

# Register your models here.
class CommonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Army)

class FactionAdmin(CommonAdmin):
    pass
admin.site.register(Faction, FactionAdmin)

class FactionTabular(admin.TabularInline):
    model = Faction
    
class GameAdmin(CommonAdmin):
    inlines = [FactionTabular,]
    
admin.site.register(Game, GameAdmin)
