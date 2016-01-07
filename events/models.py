from personnel.models import Company, MsLevel

from django.db import models
from datetime import datetime

class Event(models.Model):
    event_type = models.ForeignKey(EventType, related_name='event')
    date = models.DateTimeField(null=False, default=datetime.today())
    required_companies = models.ManyToManyField(Company, default='')
    required_ms_levels = models.ManyToManyField(MsLevel, default='')
    is_required = models.BooleanField(default=True)

    def __unicode__(self):
        format = self.date.strftime('%d %b, %Y')
        return "%s: %s" % (self.event_type, format)


class EventType(models.Model):
    type = models.CharField(max_length=150)

    def __unicode__(self):
        return self.type


class Attended(models.Model):
    attended_list = models.ManyToManyField('personnel.Cadet', default='', null=False)
    event = models.OneToOneField('Event', blank=False, null=True)

    def __unicode__(self):
        return "Attendance: " + str(self.event)

