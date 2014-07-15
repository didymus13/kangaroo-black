from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^send/(?P<campaign_id>[0-9]+)/$', views.send_invitation, name='send'),
    url(r'^accept/(?P<uuid>.+)/$', views.accept_invitation, name='accept'),
)
