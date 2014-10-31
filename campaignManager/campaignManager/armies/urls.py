from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^game/(?P<pk>\d+)/factions/$', views.get_game_factions, name='get_game_factions'),
)
