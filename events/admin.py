from django.contrib import admin
from Event.models import Attended, Event

class AttendedAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attended, AttendedAdmin)

class EventAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventAdmin)