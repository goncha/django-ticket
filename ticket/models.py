# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class CustomerArea(models.Model):
    class Meta:
        managed = False
        db_table = 'tb_area'
        verbose_name = _('customer area')
        verbose_name_plural = _('customer areas')

    city = models.CharField(_('city'), max_length=32)
    district = models.CharField(_('district'), max_length=32)
    province = models.CharField(_('province'), max_length=32)
    address = models.CharField(_('address'), max_length=128)

    def __unicode__(self):
        return self.address


class Customer(models.Model):
    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    phone = models.CharField(_('customer phone'), max_length=16)
    area_id = models.BigIntegerField(_('area ref'))
    nick_name = models.CharField(_('customer name'), max_length=32)

    def __unicode__(self):
        return self.phone


class Problem(models.Model):
    '''问题类型：安装、注册、账户密码、登录、积分等'''
    class Meta:
        verbose_name = _('problem')
        verbose_name_plural = _('problems')

    name = models.CharField(_('name'), max_length=16, unique=True)
    owner_group = models.ForeignKey(Group, verbose_name=_('owner group'), related_name='+')
    owner = models.ForeignKey(User, verbose_name=_('owner'), related_name='+')

    def __unicode__(self):
        return self.name


class Channel(models.Model):
    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    name = models.CharField(_('name'), max_length=16, unique=True)

    def __unicode__(self):
        return self.name


class Ticket(models.Model):
    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = (
        (STATUS_OPEN, _('Open')),
        (STATUS_CLOSED, _('Closed')),
    )

    SOLUTION_CUSTOMER = 'customer'
    SOLUTION_SERVICE = 'service'
    SOLUTION_PRODUCT = 'product'
    SOLUTION_OPERATION = 'operation'
    SOLUTION_LIST = (
        (SOLUTION_CUSTOMER, _('Customer Group')),
        (SOLUTION_SERVICE, _('Service Group')),
        (SOLUTION_PRODUCT, _('Product Group')),
        (SOLUTION_OPERATION, _('Operation Group')),
    )

    customer_id = models.BigIntegerField(_('customer ref'))
    phone = models.CharField(_('customer phone'), max_length=16)
    name = models.CharField(_('customer name'), max_length=16)
    area_id = models.BigIntegerField(_('area ref'))
    area_name = models.CharField(_('customer area'), max_length=128)
    building = models.CharField(_('building'), max_length=16)
    room = models.CharField(_('room'), max_length=16)
    device_model = models.CharField(_('device model'), max_length=16)
    device_os = models.CharField(_('device os'), max_length=16)
    summary = models.CharField(_('summary'), max_length=64)
    description = models.TextField(_('description'), blank=True)
    problem = models.ForeignKey(Problem, verbose_name=_('problem'), related_name='+')
    channel = models.ForeignKey(Channel, verbose_name=_('channel'), related_name='+')
    solution = models.CharField(_('solution'), max_length=16, choices=SOLUTION_LIST, default=SOLUTION_SERVICE)
    status = models.CharField(_('status'), max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)
    create_time = models.DateTimeField(_('create time'))
    modify_time = models.DateTimeField(_('modify time'))
    creator = models.ForeignKey(User, verbose_name=_('creator'), related_name='+')
    modifier = models.ForeignKey(User, verbose_name=_('modifier'), related_name='+', null=True, blank=True)

    def __unicode__(self):
        return self.summary

    def get_absolute_url(self):
        return reverse('ticket:detail', args=(self.id,))


class Comment(models.Model):
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    ticket = models.ForeignKey(Ticket, verbose_name=_('ticket'), related_name='comment_set')
    author = models.ForeignKey(User, verbose_name=_('author'), related_name='+')
    content = models.TextField(_('content'))
    create_time = models.DateTimeField(_('create time'))


class Visit(models.Model):
    class Meta:
        verbose_name = _('visit')
        verbose_name_plural = _('visits')

    STATUS_OK = 1
    STATUS_NO_ANSWER = 2
    STATUS_DECLINE = 3
    STATUS_BUSY = 4
    STATUS_CLOSED = 5
    STATUS_OFF = 6

    STATUS_CHOICES = (
        (STATUS_OK, _('OK')),
        (STATUS_NO_ANSWER, _('No answer')),
        (STATUS_DECLINE, _('Decline')),
        (STATUS_BUSY, _('Busy')),
        (STATUS_CLOSED, _('Stopped')),
        (STATUS_OFF, _('Off')),
    )

    ticket = models.ForeignKey(Ticket, verbose_name=_('ticket'), related_name='visit_set')
    author = models.ForeignKey(User, verbose_name=_('author'), related_name='+')
    content = models.TextField(_('content'), blank=True)
    create_time = models.DateTimeField(_('create time'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_OK)
