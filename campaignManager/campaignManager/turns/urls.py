from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<turn_id>[0-9]+)/issue_challenge/(?P<challenger_id>[0-9]+)/(?P<recepient_id>[0-9]+)/$', 
        views.issue_challenge, name='challenge_new'),
    url(r'^new_turn/(?P<campaign_id>[0-9]+)/$', views.new_turn, name='new_turn'),
)
