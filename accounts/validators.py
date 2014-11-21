# -*- coding: utf-8 -*-

import re

from django.core.validators import RegexValidator

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

class TelValidator(RegexValidator):
    message = _("Enter a valid tel number")
    regex = re.compile(r"^(?:(?:\+?\d+[- ])?\d+[- ])?\d{6,11}$")

validate_tel = TelValidator()


# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
