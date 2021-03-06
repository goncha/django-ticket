from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ticketsys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'ticketsys.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^ticket/', include('ticket.urls', namespace='ticket')),
)
