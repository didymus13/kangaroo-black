from django.contrib import admin
from webbrowser import register
from models import *

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'live_date', 'modified_date', 'published')
    list_filter = ('author', 'published', 'live_date', 'modified_date')
    prepopulated_fields = {'slug': ('title',)}
