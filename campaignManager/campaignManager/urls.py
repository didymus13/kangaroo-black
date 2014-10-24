from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

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
            form_class=UserCreationForm,
            success_url='/login'
    ), name='register'),
    url(r'^$', 'campaignManager.profiles.views.home', name='home'),
    url('^profile/', include('campaignManager.profiles.urls', namespace='profile')),
    url('^campaigns/', include('campaignManager.campaigns.urls', namespace='campaigns')),
    url('^invitations/', include('campaignManager.invitations.urls', namespace='invitations')),
    url('^turns/', include('campaignManager.turns.urls', namespace='turns')),
)
