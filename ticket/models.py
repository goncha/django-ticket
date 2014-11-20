# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse


class CustomerArea(models.Model):
    class Meta:
        managed = False
        db_table = 'tb_area'

    city = models.CharField(max_length=32)
    district = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    address = models.CharField(max_length=128)

    def __unicode__(self):
        return self.address


class Customer(models.Model):
    class Meta:
        managed = False
        db_table = 'user'

    phone = models.CharField(max_length=16)
    area_id = models.BigIntegerField()
    nick_name = models.CharField(max_length=32)
    real_name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.phone


class Problem(models.Model):
    '''问题类型：安装、注册、账户密码、登录、积分等'''
    name = models.CharField(max_length=16, unique=True)
    owner_group = models.ForeignKey(Group, related_name='+')
    owner = models.ForeignKey(User, related_name='+')

    def __unicode__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.name

class Ticket(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    )

    SOLUTION_CUSTOMER = 'customer'
    SOLUTION_SERVICE = 'service'
    SOLUTION_PRODUCT = 'product'
    SOLUTION_OPERATION = 'operation'
    SOLUTION_LIST = (
        (SOLUTION_CUSTOMER, 'Customer'),
        (SOLUTION_SERVICE, 'Service'),
        (SOLUTION_PRODUCT, 'Product'),
        (SOLUTION_OPERATION, 'Operation'),
    )

    user_id = models.BigIntegerField()
    user_phone = models.CharField(max_length=16, )
    user_name = models.CharField(max_length=16)
    area_id = models.BigIntegerField()
    area_name = models.CharField(max_length=128)
    building = models.CharField(max_length=16)
    room = models.CharField(max_length=16)
    device_model = models.CharField(max_length=16)
    device_os = models.CharField(max_length=16)
    summary = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    problem = models.ForeignKey(Problem, related_name='+')
    channel = models.ForeignKey(Channel, related_name='+')
    solution = models.CharField(max_length=16, choices=SOLUTION_LIST, default=SOLUTION_SERVICE)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    creator = models.ForeignKey(User, related_name='+')
    modifier = models.ForeignKey(User, related_name='+', null=True, blank=True)

    def __unicode__(self):
        return self.summary

    def get_absolute_url(self):
        return reverse('ticket:detail', args=(self.id,))



class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comment_set')
    author = models.ForeignKey(User, related_name='+')
    content = models.TextField()
    create_time = models.DateTimeField()


class Visit(models.Model):
    STATUS_OK = 1
    STATUS_NO_ANSWER = 2
    STATUS_DECLINE = 3
    STATUS_BUSY = 4
    STATUS_CLOSED = 5
    STATUS_OFF = 6

    STATUS_CHOICES = (
       (STATUS_OK, 'OK'),
       (STATUS_NO_ANSWER, 'No Answer'),
       (STATUS_DECLINE, 'Decline'),
       (STATUS_BUSY, 'Busy'),
       (STATUS_CLOSED, 'Closed'),
       (STATUS_OFF, 'Off'),
    )

    ticket = models.ForeignKey(Ticket, related_name='visit_set')
    author = models.ForeignKey(User, related_name='+')
    content = models.TextField(blank=True)
    create_time = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OK)
