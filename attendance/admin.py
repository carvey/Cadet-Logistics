from django.contrib import admin
from attendance.models import Attended, Event

class AttendedAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attended, AttendedAdmin)

class EventAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventAdmin)