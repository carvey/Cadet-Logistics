from django.db import models
from datetime import datetime
from eagletrack.models import MsLevel

class PtTest(models.Model):
    date = models.DateField(default=datetime.today(), blank=False)
    MsLevelFour = models.BooleanField(default=False, help_text='Check this box if this test is only for MS4s.')
    MSLevelThree = models.BooleanField(default=False, help_text='Check this box if this test is only for MS3s')
    
    def __unicode__(self):
        format_date = self.date.strftime('%d %b, %Y')
        return '%s PT test' % format_date
    
    class Meta:
        db_table='PtTest'
        
def get_ms_level(ms):
    if ms is 'MS4':
        return MsLevel.objects.get(name='MS4')
    elif ms is 'MS3':
        return MsLevel.objects.get(name='MS3')
        
class PtScore(models.Model):
    ms4 = get_ms_level('MS4')
    ms3 = get_ms_level('MS3')
        
    pt_test = models.ForeignKey(PtTest, default='', blank=False, null=False)
    grader = models.ForeignKey('eagletrack.Cadet', related_name='grader', blank=False, null=True, limit_choices_to={'eagletrack.ms_level':ms4, 'eagletrack.ms_level':ms3})
    cadre_grader=models.ForeignKey('eagletrack.Cadre', blank=True, null=True)
    cadet = models.ForeignKey('eagletrack.Cadet', related_name='cadet_score', blank=False)
    pushups = models.PositiveIntegerField(default=0)
    situps = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):  
        format_date = self.pt_test.date.strftime('%d %b, %Y')
        return 'PT Score %s for cadet: %s' % (format_date, self.cadet)
    
    
    class Meta:
        db_table='PtScore'
        
class Time(models.Model):
    pt_score = models.ForeignKey(PtScore, related_name='pt_score', default='', blank=False)
    minutes = models.PositiveIntegerField(default=0)
    seconds = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return 'Time - %s:%s' % (self.minutes, self.seconds)
    
    class Meta:
        db_table='Time'
        verbose_name="Two Mile time"
        verbose_name_plural="Two Mile time"