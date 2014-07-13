import ast, collections

from django.db import models
from datetime import datetime
from personnel.models import MsLevel
from django.core.validators import RegexValidator

male='Male'
female='Female'
GENDER_CHOICES =(
                 (male, 'Male'),
                 (female, 'Female')
                 )
group_1='17-21'
group_2='22-26'
group_3='27-31'
group_4='32-36'
group_5='37-41'
group_6='42-46'
group_7='47-51'
group_8='52-56'

AGE_GROUPS=(
            (group_1, '17-21'),
            (group_2, '22-26'),
            (group_3, '27-31'),
            (group_4, '32-36'),
            (group_5, '37-41'),
            (group_6, '42-46'),
            (group_7, '47-51'),
            (group_8, '52-56')
            )
pushups='Pushups'
situps='Situps'
two_mile='Two-mile run'
ACTIVITY_CHOICES=(
                  (pushups, 'Pushups'),
                  (situps, 'Situps'),
                  (two_mile, 'Two-mile run')
                  )

#This class handles the pt test itself, identified by a date
class PtTest(models.Model):
    date = models.DateField(default=datetime.today(), blank=False)
    MsLevelFour = models.BooleanField(default=False, help_text='Check this box if the MS4 class will be taking this test')
    MsLevelThree = models.BooleanField(default=True, help_text='Check this box if the MS3 class will be taking this test')
    MsLevelTwo= models.BooleanField(default=True, help_text='Check this box is the MS2 class will be taking this test')
    MsLevelOne = models.BooleanField(default=True, help_text='Check this box if the MS1 class will be taking this test')
    
    def __unicode__(self):
        format_date = self.date.strftime('%d %b, %Y')
        return '%s PT Test' % format_date
    
    class Meta:
        db_table='PtTest'  

#The PTscore information for each cadet. Indentified by a foreign key linking to a specific cadet
class PtScore(models.Model):
    grader = models.ForeignKey('personnel.Cadet', related_name='grader', blank=False, null=True) 
    pt_test = models.ForeignKey(PtTest, default='', blank=False, null=False)
    cadre_grader=models.ForeignKey('personnel.Cadre', blank=True, null=True)
    cadet = models.ForeignKey('personnel.Cadet', related_name='cadet_score', blank=False)
    score = models.PositiveIntegerField(default=0)
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
    
    '''
    Helper method to return the run time with 
    a zero place holder if the minutes has 
    only one number. So a time of 15:4 will 
    be returned as 15:04.
    '''
    def get_run_time_str(self):
        time = self.get_run_time()
        return '%02d:%02d' % (time[0], time[1])
    
    def get_pt_test(self):
        return self.pt_test
    
    def get_pushups(self):
        return self.pushups
    
    def get_situps(self):
        return self.situps
    
    '''
    Helper method to get the two mile time 
    in minutes for computation. So a time of 
    15:43 will be returned as 15.72 minutes
    '''
    def get_two_mile_min(self):
        time_list = self.get_run_time()
        minutes = time_list[0]
        seconds = time_list[1]
        return minutes + (seconds/60.0)
        

    class Meta:
        db_table='PtScore'
        
class Grader(models.Model):
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False, null=True)
    activity = models.CharField(max_length=15,choices=ACTIVITY_CHOICES, blank=False, null=True)
    age_group = models.CharField(max_length=5, choices=AGE_GROUPS, blank=False, null=True)
    score_table = models.TextField(default="'number pushups or situps/time' : 'grade', \
        'number pushups or situps/time' : 'grade'", blank=False)
    
    def __unicode__(self):
        return '%s grader for %s (%s)' % (self.activity, self.gender, self.age_group)
    def get_score_dict(self):
        return ast.literal_eval("{%s}" % self.score_table)
    def get_ordered_dict(self):
        return collections.OrderedDict(sorted(self.get_score_dict().items()))
    def get_first(self):
        ordered_dict = self.get_ordered_dict()
        return next(ordered_dict.iterkeys())
    def get_last(self):
        ordered_dict = self.get_ordered_dict()
        return next(reversed(ordered_dict))