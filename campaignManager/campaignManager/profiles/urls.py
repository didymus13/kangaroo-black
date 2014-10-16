from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<username>\w+)/$', views.detail, name='detail'),
    url(r'^(?P<username>\w+)/edit/$', views.edit, name='edit'),
)
