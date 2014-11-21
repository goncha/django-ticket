# -*- coding: utf-8 -*-

from django.forms.fields import CharField

from accounts import widgets
from accounts import validators


class TelField(CharField):
    widget = widgets.TelInput
    default_validators = [validators.validate_tel]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(TelField, self).clean(value)


# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
