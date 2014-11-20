# -*- coding: utf-8 -*-

from django import forms

from ticket.models import Ticket

class TicketForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    area_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Ticket
        exclude = ['create_time', 'modify_time', 'creator', 'modifier']




# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
