# -*- coding: utf-8 -*-

from django import forms

from accounts.models import UserProfile
from accounts.fields import TelField

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField()
    phone = TelField()

    class Meta:
        model = UserProfile
        exclude = ['user']

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
