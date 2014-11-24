from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')


    user = models.ForeignKey(User, verbose_name=_('user'), related_name='user_profile_set')
    email = models.CharField(_('email'), max_length=64)
    phone = models.CharField(_('mobile phone'), max_length=32)

    def __unicode__(self):
        return '%s, %s, %s' % (user.username, email, phone,)
