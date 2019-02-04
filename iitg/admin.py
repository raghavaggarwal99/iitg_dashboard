from django.contrib import admin

# Register your models here.

from .models import Event,Student,Page, Deadline

admin.site.register(Event)
admin.site.register(Student)
admin.site.register(Page)
admin.site.register(Deadline)
