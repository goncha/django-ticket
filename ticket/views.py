from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
@login_required
def home(request):
    context = {}
    return render(request, 'ticket/home.html', context)
