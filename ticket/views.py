# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from ticket.models import Ticket, Visit, Comment, Customer, CustomerArea
from ticket.forms import TicketForm

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
    form = TicketForm(instance=get_object_or_404(Ticket, pk=ticket_id))
    return render(request, 'ticket/ticket.html', {'form': form})


@require_http_methods(['POST'])
@login_required
def comment(request):
    return render(request, 'ticket/ticket.html')


@require_http_methods(['GET', 'POST'])
@login_required
def visit(request):
    return render(request, 'ticket/ticket.html')


@require_http_methods(['GET'])
@login_required
def index(request):
    context = {}
    context['ticket_list'] = Ticket.objects.all()

    return render(request, 'ticket/list.html', context)


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
