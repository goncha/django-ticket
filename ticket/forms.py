# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from ticket.models import Ticket, Problem, Visit

class TicketForm(forms.ModelForm):
    customer_id = forms.IntegerField(widget=forms.HiddenInput())
    area_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Ticket
        exclude = ['create_time', 'modify_time', 'creator', 'modifier', 'solution', 'solver', 'solve_time']


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['content', 'status']


def get_problem_choices():
    return [(p.id, p.name) for p in Problem.objects.all()]


class TicketQueryForm(forms.Form):
    begin_date = forms.DateField(label=_('Begin Date'), required=False)
    end_date = forms.DateField(label=_('End Date'), required=False)
    problem = forms.ChoiceField(label=_('Problem'), choices=get_problem_choices(), required=False)
    need_support = forms.BooleanField(label=_('Need support'), required=False)
    status = forms.ChoiceField(label=_('Status'), choices=Ticket.STATUS_CHOICES, required=False)

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
