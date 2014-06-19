from django.db import models
from datetime import datetime
from eagletrack.models import MsLevel
from django.core.validators import RegexValidator

#This class handles the pt test itself, identified by a date
class PtTest(models.Model):
    date = models.DateField(default=datetime.today(), blank=False)
    MsLevelFour = models.BooleanField(default=False, help_text='Check this box if the MS4 class will be taking this test')
    MSLevelThree = models.BooleanField(default=True, help_text='Check this box if the MS3 class will be taking this test')
    MsLevelTwo= models.BooleanField(default=True, help_text='Check this box is the MS2 class will be taking this test')
    MsLevelOne = models.BooleanField(default=True, help_text='Check this box if the MS1 class will be taking this test')
    
    def __unicode__(self):
        format_date = self.date.strftime('%d %b, %Y')
        return '%s PT test' % format_date
    
    class Meta:
        db_table='PtTest'
        
        
#These variables get the MsLevel objects themselves for use in limiting the choices of the grader field in PtScore
ms4 = MsLevel.objects.get(name='MS4')
ms3 = MsLevel.objects.get(name='MS3')   

#The PTscore information for each cadet. Indentified by a foreign key linking to a specific cadet
class PtScore(models.Model):
    pt_test = models.ForeignKey(PtTest, default='', blank=False, null=False)
    grader = models.ForeignKey('eagletrack.Cadet', related_name='grader', blank=False, null=True, limit_choices_to={'ms_level':ms4, 'ms_level':ms3})
    cadre_grader=models.ForeignKey('eagletrack.Cadre', blank=True, null=True)
    cadet = models.ForeignKey('eagletrack.Cadet', related_name='cadet_score', blank=False)
    pushups = models.PositiveIntegerField(default=0)
    situps = models.PositiveIntegerField(default=0)
    two_mile = models.CharField(max_length=5, null=True, validators=[
                                                          RegexValidator(
                                                                         regex='^[0-5]?[0-9]:[0-5]?[09]',
                                                                         message="Time must be in the mm:ss format",
                                                                         code="Invalid_time_format"
                                                                         ),
                                                          ])
    
    def __unicode__(self):  
        format_date = self.pt_test.date.strftime('%d %b, %Y')
        return 'PT Score %s for cadet: %s' % (format_date, self.cadet)
    
    
    """
    This method takes the two_mile info (CharField) of the cadet at hand and splits it into a list
    So a time of 15:43 should return a list value of [15, 43]
    """
    def get_run_time(self):
        time = str(self.two_mile)
        split_time = time.split(':')
        split_time = [int(x) for x in split_time]
        return split_time
    
    class Meta:
        db_table='PtScore'
        