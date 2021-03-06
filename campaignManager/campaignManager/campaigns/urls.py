from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<pk>[0-9]+)/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^new/$', views.edit, name='new'),
    
    url(r'^mine/$', views.my_index, name='mine'),
    url(r'^looking-for-players/$', views.looking_for_players, name='looking_for_players'),
    url(r'^(?P<slug>.+)/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
)
