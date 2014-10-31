from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<username>\w+)/$', views.detail, name='detail'),
    url(r'^(?P<username>\w+)/edit/$', views.edit, name='edit'),
    
    url(r'^(?P<username>\w+)/campaign_profile/(?P<campaign_id>\d+)/edit/', 
        views.campaign_profile_edit, name='campaign_profile_edit'),
)
