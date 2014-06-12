
from django.db import models
from datetime import datetime

class PtTest(models.Model):
    date = models.DateField(default=datetime.today(), blank=False)
    MsLevelFour = models.BooleanField(default=False, help_text='Check this box if this test is only for MS4.')
    
    def __unicode__(self):
        return '%s PT test' % self.date
    
    class Meta:
        db_table='PtTest'
        
class PtScore(models.Model):
    pt_test = models.ForeignKey(PtTest, default='', blank=False, null=False)
    cadet = models.ForeignKey('eagletrack.Cadet', related_name="score_to_cadet", blank=False)
    
    def __unicode__(self):
        return 'PtScore for cadet: %s' % self.cadet
    
    class Meta:
        db_table='PtScore'