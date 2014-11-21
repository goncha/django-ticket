# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from ticket.models import Ticket, Visit, Comment, Customer, CustomerArea
from ticket.forms import TicketForm, TicketQueryForm, CommentForm, VisitForm


@require_http_methods(['GET', 'POST'])
@login_required
def new(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            instance = form.instance
            instance.creator = request.user
            instance.modifier = instance.creator
            instance.create_time = timezone.now()
            instance.modify_time = instance.create_time
            instance.save()
            return redirect(instance)
    else:
        form = TicketForm()
    return render(request, 'ticket/ticket.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def detail(request, ticket_id):
    instance = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'GET':
        form = TicketForm(instance=instance)
    else:
        form = TicketForm(request.POST)
        if form.is_valid():
            new_instance = form.instance
            new_instance.pk = instance.pk
            new_instance.creator = instance.creator
            new_instance.create_time = instance.create_time
            new_instance.modifier = request.user
            new_instance.modify_time = timezone.now()
            new_instance.save()

            return redirect(form.instance)
    return render(request, 'ticket/ticket.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.instance
            instance.author = request.user
            instance.ticket = ticket
            instance.create_time = timezone.now()
            instance.save()
            form = CommentForm()
    else:
        form = CommentForm()

    comment_list = Comment.objects.filter(ticket=ticket)

    paginator = Paginator(comment_list, 10)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    return render(request, 'ticket/comment_list.html', {
        'ticket': ticket,
        'form': form,
        'comments': comments,
    })


@require_http_methods(['GET', 'POST'])
@login_required
def visit(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            instance = form.instance
            instance.author = request.user
            instance.ticket = ticket
            instance.create_time = timezone.now()
            instance.save()
            form = VisitForm()
    else:
        form = VisitForm()

    visit_list = Visit.objects.filter(ticket=ticket)

    paginator = Paginator(visit_list, 10)
    page = request.GET.get('page')
    try:
        visits = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        visits = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        visits = paginator.page(paginator.num_pages)

    return render(request, 'ticket/visit_list.html', {
        'ticket': ticket,
        'form': form,
        'visits': visits,
    })


@require_http_methods(['GET'])
@login_required
def index(request):
    form = TicketQueryForm(request.GET)
    if form.is_valid():
        ticket_list = Ticket.objects.all()
    else:
        ticket_list = []

    paginator = Paginator(ticket_list, 10)
    page = request.GET.get('page')
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tickets = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        tickets = paginator.page(paginator.num_pages)

    return render(request, 'ticket/list.html', {
        'tickets': tickets,
        'form': form,
    })


@require_http_methods(['GET'])
@login_required
def customer(request, phone):
    values = []
    for customer in Customer.objects.filter(phone=phone):
        values.append({'id': customer.id,
                       'area_id': customer.area_id,
                       'nick_name': customer.nick_name,
                       'real_name': customer.real_name,
                       'phone': customer.phone})
    return JsonResponse({'values': values})


@require_http_methods(['GET'])
@login_required
def customer_area(request, area_id):
    area_id = int(area_id)
    if area_id == -1:
        area = CustomerArea(address='Dafeng', city='Shanghai', district='Songjiang', province='Shanghai')
        area.id = area_id
    elif area_id == 0:
        area = CustomerArea(address='Unknown Address', city='Unknown City',
                            district='Unknown District', province='Unknown Province')
        area.id = area_id
    else:
        area = get_object_or_404(CustomerArea, pk=area_id);
    value = {'id': area.id,
             'address': area.address,
             'city': area.city,
             'province': area.province,
             'district': area.district}
    return JsonResponse({'values': [value]})

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
