from django.contrib import admin

from ticket.models import Channel, Problem

admin.site.register(Channel, admin.ModelAdmin)
admin.site.register(Problem, admin.ModelAdmin)
