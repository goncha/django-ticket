# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from ticket import views

urlpatterns = patterns('ticket.views',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<ticket_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<ticket_id>\d+)/comment/$', views.comment, name='comment'),
    url(r'^(?P<ticket_id>\d+)/visit/$', views.visit, name='visit'),
    url(r'^customer/(?P<phone>\d+)/$', views.customer, name='customer'),
    url(r'^customer_area/(?P<area_id>-?\d+)/$', views.customer_area, name='customer_area'),
)

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
