from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='+')
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)

    def __unicode__(self):
        return '%s, %s, %s' % (user.username, email, phone,)
