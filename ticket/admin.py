from django.contrib import admin

from ticket.models import Channel, Problem, Solution

admin.site.register(Channel, admin.ModelAdmin)
admin.site.register(Problem, admin.ModelAdmin)
admin.site.register(Solution, admin.ModelAdmin)
