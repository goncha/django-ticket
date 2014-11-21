# -*- coding: utf-8 -*-

from django import forms

from ticket.models import Ticket, Problem

class TicketForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    area_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Ticket
        exclude = ['create_time', 'modify_time', 'creator', 'modifier']


def get_problem_choices():
    return [(p.id, p.name) for p in Problem.objects.all()]


class TicketQueryForm(forms.Form):
    summary = forms.CharField(label='Summary', required=False)
    begin_date = forms.DateField(label='Begin Date', required=False)
    end_date = forms.DateField(label='End Date', required=False)
    problem = forms.ChoiceField(label='Problem', choices=get_problem_choices(), required=False)
    solution = forms.ChoiceField(label='Solution', choices=Ticket.SOLUTION_LIST, required=False)
    status = forms.ChoiceField(label='Status', choices=Ticket.STATUS_CHOICES, required=False)

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
