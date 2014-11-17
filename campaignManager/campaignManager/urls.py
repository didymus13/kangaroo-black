from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from campaignManager.profiles.models import MyUserCreationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campaignManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url('^register/$', CreateView.as_view(
            template_name='form.html',
            form_class=MyUserCreationForm,
            success_url='/login'
    ), name='register'),
    url(r'^$', 'campaignManager.blog.views.home', name='home'),
    url('^blog/', include('campaignManager.blog.urls', namespace='blog')),
    url('^profile/', include('campaignManager.profiles.urls', namespace='profile')),
    url('^campaigns/', include('campaignManager.campaigns.urls', namespace='campaigns')),
    url('^invitations/', include('campaignManager.invitations.urls', namespace='invitations')),
    url('^turns/', include('campaignManager.turns.urls', namespace='turns')),
    url('^armies/', include('campaignManager.armies.urls', namespace='armies')),
)
