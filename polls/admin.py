from django.contrib import admin

from .models import Choice, Poll, Question

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
