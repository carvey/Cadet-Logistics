from personnel.models import Company, MsLevel

from django.db import models
from datetime import datetime

'''Static variables'''
ONE = 'one'
TWO = 'two'
THREE = 'three'
FOUR = 'four'
MS_LEVEL_CHOICES = (
            (ONE, 'MS1'),
            (TWO, 'MS2'),
            (THREE, 'MS3'),
            (FOUR, 'MS4'),
            )

generic_event='generic_event'
pt_event = 'pt_event'
lab_event = 'lab_event'
class_event = 'class_event'
ftx_event = 'ftx_event'
EVENT_TYPES = (
              (pt_event, 'PT'),
              (class_event, 'Class'),
              (lab_event, 'Lab'),
              (generic_event, 'Generic Event'),
              (ftx_event, 'FTX'),
              )

class Attended(models.Model):
    attended_list = models.ManyToManyField('personnel.Cadet', default='', null=False)
    event = models.OneToOneField('Event', blank=False, null=True)
    
    def __unicode__(self):
        return "Attendance: " + str(self.event)

class Event(models.Model):
    event_type = models.CharField(max_length = 15, choices=EVENT_TYPES, blank=False)
    date = models.DateTimeField(null=False, default=datetime.today())
    required_companies = models.ManyToManyField(Company, default='')
    required_ms_levels = models.ManyToManyField(MsLevel, default='')
    is_required = models.BooleanField(default=True)
    
    def __unicode__(self):
        format = self.date.strftime('%d %b, %Y')
        return "%s: %s" % (self.event_type, format)
    