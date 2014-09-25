from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new_turn/(?P<campaign_id>\d+)/$', views.create, name='create'),
    url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit'),
    
    url(r'^(?P<pk>\d+)/challenge/(?P<recipient>\d+)/$', views.challenge_send, 
        name='challenge_send'),
    url(r'^(?P<pk>\d+)/challenge/(?P<uuid>.+)/$', views.challenge_accept, 
        name='challenge_accept'),
    url(r'^(?P<pk>\d+)/challenge/(?P<uuid>.+)/(?P<winner>\d+)/$', views.challenge_complete, 
        name='challenge_complete'),
)
