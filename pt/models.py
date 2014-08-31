import ast, collections

from itertools import cycle

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
    cadet = models.ForeignKey('personnel.Cadet', related_name='cadet_score', blank=False)
    pt_test = models.ForeignKey(PtTest, default='', blank=False, null=False)
    grader = models.ForeignKey('personnel.Cadet', related_name='grader', blank=False, null=True)
    cadre_grader=models.ForeignKey('personnel.Cadre', blank=True, null=True)

    pushups = models.PositiveIntegerField(default=0)
    situps = models.PositiveIntegerField(default=0)
    two_mile = models.CharField(max_length=5, null=True, validators=[
                                                          RegexValidator(
                                                                         regex='^[0-5]?[0-9]:[0-5]?[0-9]',
                                                                         message="Time must be in the mm:ss format",
                                                                         code="Invalid_time_format"
                                                                         ),
                                                          ])

    score = models.PositiveIntegerField(default=0)
    pushups_score = models.PositiveIntegerField(default=0)
    situps_score = models.PositiveIntegerField(default=0)
    run_score = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):  
        format_date = self.pt_test.date.strftime('%d %b, %Y')
        return 'PT Score %s for cadet: %s' % (format_date, self.cadet)
    
    def save(self, *args, **kwargs):
        try:
            age_group = self.get_age_group()
            # Gets the graders for the cadet
            pushups_grader = Grader.objects.filter(age_group=age_group, gender=self.cadet.gender, activity='Pushups')[0]
            situps_grader = Grader.objects.filter(age_group=age_group, gender=self.cadet.gender, activity='Situps')[0]
            two_mile_grader = Grader.objects.filter(age_group=age_group, gender=self.cadet.gender, activity='Two-mile run')[0]

            # Sets the score to zero to prevent the score increasing each time the object
            # is saved, if there is already a score
            self.score = 0

            # Get the score dictionary from the pushups grader object
            pushups_score_dict = pushups_grader.get_ordered_dict()
            # Format the value to have a leading 0 if it is a single digit
            # This is the key used to check if the value is in the dictionary of grades
            string_pushups = "%02d" % self.pushups
            # Check to see if the number of pushups for the PtScore object is
            # in the list of keys. If it is then we use the pushups value as the key to get the grade.
            if string_pushups in pushups_score_dict.keys():
                score_from_dict = int(pushups_score_dict[string_pushups])
                self.pushups_score = score_from_dict
                self.score += score_from_dict
            # The value of pushups was not found in the keys so we determine if it was below the lowest
            # or above the highest pushups value
            else:
                if float(self.pushups) < float(pushups_grader.get_first()):
                    self.pushups_score = 0
                    self.score += self.pushups_score
                elif float(self.pushups) > float(pushups_grader.get_last()):
                    self.pushups_score = 100
                    self.score += self.pushups_score

            # Get the score dictionary from the situps grader object
            situps_score_dict = situps_grader.get_ordered_dict()

            # Format the value to have a leading 0 if it is a single digit
            # This is the key used to check if the value is in the dictionary of grades
            string_situps = "%02d" % self.situps
            # Check to see if the number of situps for the PtScore object is
            # in the list of keys. If it is then we use the situps value as the key to get the grade.
            if string_situps in situps_score_dict.keys():
                score_from_dict = int(situps_score_dict[string_situps])
                self.situps_score = score_from_dict
                self.score += self.situps_score

            # The value of situps was not found in the keys so we determine if it was below the lowest
            # or above the highest situps value
            else:
                if float(self.situps) < float(situps_grader.get_first()):
                    self.situps_score = 0
                    self.score += self.situps_score
                elif float(self.situps) > float(pushups_grader.get_last()):
                    self.situps_score = 100
                    self.score += self.situps_score

            # Calculate the two-mile score
            self.run_score = int(self.get_run_score(two_mile_grader))
            self.score += self.run_score

        except IndexError:
            #this will catch an index error to avoid errors when running scripted db population
            pass
        
        # Call the actual save method to save the score in the database
        super(PtScore, self).save(*args, **kwargs)

    def get_run_time(self):
        """
         This method takes the two_mile info (CharField) of the cadet at hand and splits it into a list
         So a time of 15:43 should return a list value of [15, 43]
        """
        time = str(self.two_mile)
        split_time = time.split(':')
        split_time = [int(x) for x in split_time]
        return split_time

    def get_run_time_str(self):
        '''
         Helper method to return the run time with
         a zero place holder if the minutes has
         only one number. So a time of 15:4 will
         be returned as 15:04.
        '''
        time = self.get_run_time()
        return '%02d:%02d' % (time[0], time[1])
    
    def get_pt_test(self):
        return self.pt_test
    
    def get_pushups(self):
        return self.pushups
    
    def get_situps(self):
        return self.situps

    def get_two_mile_min(self):
        '''
         Helper method to get the two mile time
         in minutes for computation. So a time of
         15:43 will be returned as 15.72 minutes
        '''
        time_list = self.get_run_time()
        minutes = time_list[0]
        seconds = time_list[1]
        return minutes + (seconds/60.0)

    def get_time_mins(self, time):
        '''
         Converts a given time string in the form of '[mm]:[ss]' into a decimal minutes format
         So a time of '13:30' will be returned as 13.5
        '''
        time_list = time.split(':')
        time_list = [int(t) for t in time_list]
        minutes = time_list[0]
        seconds = time_list[1]
        return minutes + (seconds/60.0)

    def convert_time_mins_secs(self, time):
        '''
         Converts a given time string from minutes into the form '[mm]:[ss]'.
         So a time of '13.5' will be returned as '13:30'
        '''
        time_split = time.split('.')
        minutes = float(time_split[0])
        formatted_seconds = (float(time) - minutes) * 60.0
        return '%02.0f:%02.0f' % (minutes, formatted_seconds)

    def get_age_group(self):
        '''
         Gets the age range that a cadet is a part of. Used for getting the correct Grader (score value) object
        '''
        score_values=Grader.objects.all()
        
        cadet_age = self.cadet.age
        for score_value in score_values:
            value = score_value.age_group.split('-')
            if cadet_age >= int(value[0]) and cadet_age <= int(value[1]):
                return score_value.age_group      

    def get_run_score(self,two_mile_grader):
        '''
         Used to calculate the score for two-mile run
        '''
        # Gets the list of keys in minute format, so a key of '17:30' will be represented
        # as '17.5'
        times_in_mins_list = [self.get_time_mins(time) for time in two_mile_grader.get_ordered_dict()]
        
        # The two-mile time for this score object, in minute format
        run_time = self.get_two_mile_min()
        
        # Creates a cycle to iterate through the key values
        times_cycle = cycle(times_in_mins_list)
        
        # Store the first time in the list, so that in the for loop we can tell when the cycle
        # is complete since the next_time will be equal to the first_time
        first_time = times_in_mins_list[0]
        
        # Gets the next time in the list before we begin the loop
        next_time = times_cycle.next()
        
        # Time key defaults to zero
        time_key = 0
        
        # Iterate through the list of keys
        for time in times_in_mins_list:
            # Get the current time object in the list, and also the next time object
            this_time, next_time = time, times_cycle.next()
            
            # If this is true we found an exact match, so return the current time value as the key
            if run_time == this_time:
                time_key = this_time
                
            # Check to see if our two-mile time is between this_time and next_time. Also makes sure
            # that we aren't at the end of the cycle by checking that next_time is not equal to first_time.
            # If true we return next_time as the key, since it is the slower of the two times.
            elif run_time > this_time and run_time < next_time and next_time != first_time:
                time_key = next_time
            # Checks if run_time is less than this_time and if this_time is the first time in the list.
            # If so it means they had a faster time than the fastest time on the scale, so they make a 100.
            elif run_time < this_time and this_time == first_time:
                time_key = 100
        
        # If time_key is equal to zero it means that their time was too slow and was not on the scale,
        # so they make a 0.
        if time_key == 0:
            return 0
        elif time_key == 100:
            return 100
        else:
            # Convert the key from decimal minute format back to mm:ss format
            score_key = self.convert_time_mins_secs(str(time_key))
            # Get the grade from the grader dictionary
            grade = two_mile_grader.get_ordered_dict()[str(score_key)]

            return grade
        
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