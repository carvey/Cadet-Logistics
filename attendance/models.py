from eagletrack.models import User, Company, MsLevel

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

class Event(models.Model):
    date = models.DateTimeField(null=False, default=datetime.today())
    attended_list = models.ManyToManyField(User, default='', null=False)
    required_companies = models.ManyToManyField(Company, default='')
    required_ms_levels = models.ManyToManyField(MsLevel, default='')
    is_required = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        
class GenericEvent(Event):
    name = models.CharField(max_length=50,default='')
    
    def __unicode__(self):
        return 'GenericEvent: %s, date: %s' % self.name, self.date
    
    class Meta:
        db_table='GenericEvent'
        
class PtEvent(Event):
    def __unicode__(self):
        return 'PtEvent date: %s' % self.date
    
    class Meta:
        db_table='PtEvent'

class LabEvent(Event):
    def __unicode__(self):
        return 'LabEvent date: %s' % self.date
    class Meta:
        db_table='LabEvent'
        
class ClassEvent(Event):
    def __unicode__(self):
        return 'ClassEvent date: %s' % self.date
    class Meta:
        db_table='ClassEvent'