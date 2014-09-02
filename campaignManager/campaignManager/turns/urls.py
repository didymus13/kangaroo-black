from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new_turn/(?P<campaign_id>[0-9]+)/$', views.create, name='create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
)
