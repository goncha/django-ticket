# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
@login_required
def home(request):
    return render(request, 'ticketsys/site.html')

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
