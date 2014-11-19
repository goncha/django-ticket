# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('ticket.views',
   url(r'^$', 'home', name='home'),
)


# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
