from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index/(?P<slug>.+)/$', views.index, name='index'),
    url(r'^edit/$', views.edit, name='new')
)
