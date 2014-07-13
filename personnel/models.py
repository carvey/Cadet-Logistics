
from django.core.validators import MaxValueValidator, MinValueValidator, validate_email
from django.db import models
from django.contrib.auth.models import User

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
male='Male'
female='Female'
GENDER_CHOICES =(
                 (male, 'Male'),
                 (female, 'Female')
                 )

"""Users is the base class for Cadet and Cadre"""
class Users(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 30)
    age = models.PositiveIntegerField(blank=False)
    email = models.EmailField(blank=True, validators=[validate_email])
    
    def __unicode__(self):
        return (self.last_name + ", " + self.first_name)
    
    class Meta:
        abstract = True
        
"""Company is the model for the companies in the batallion"""
class Company(models.Model):
    name = models.CharField(max_length = 10, default = "", help_text="Enter Name of the new company here")
    company_commander = models.OneToOneField('Cadet', db_index=False, related_name='ccs', limit_choices_to={'is_company_staff':True}, blank=True, null=True, help_text="Enter the Name of the Commander Officer")
    first_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="first_sgts", limit_choices_to={'is_company_staff':True}, blank=True, null=True, help_text="Enter the First Sergeant for this Company")
    
    class Meta:
        db_table='Company'
    
    def __unicode__(self):
        return self.name

"""Cadet is the model for cadets in the batallion. This model extends the Users abstract model. Each cadet should ideally be assigned to a company"""
class Cadet(Users):
    eagle_id = models.PositiveIntegerField(default=0, blank=False, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    platoon = models.ForeignKey('Platoon', blank=True, null=True)
    ms_level = models.ForeignKey('MsLevel', blank=False, null=False)
    gpa = models.DecimalField(default=4.0, max_digits=3, decimal_places=2, blank=True)
    ms_grade = models.IntegerField(default=100)
    is_staff = models.BooleanField(default = False)
    is_company_staff = models.BooleanField(default = False)
    ##
    cell_number = models.CharField(max_length=14, blank=True)
    volunteer_hours_completed = models.BooleanField(default=False)
    turned_in_104r = models.BooleanField(default=False)
    ##
    on_profile=models.BooleanField(default=False)
    profile_reason=models.CharField(max_length=250, blank=True)
    events_missed = models.PositiveIntegerField(default=0, blank=True)
    class_events_missed = models.PositiveIntegerField(default=0, blank=True)
    lab_events_missed = models.PositiveIntegerField(default=0, blank=True)
    pt_missed = models.PositiveIntegerField(default=0, blank=True)
    attendance_rate=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True) #logic for true and false attended is 100 and 0
    at_risk = models.BooleanField(default=False)
    ##
    contracted = models.BooleanField(default=False)
    smp = models.BooleanField(default=False)
    dropped = models.BooleanField(default=False)
    commissioned = models.BooleanField(default=False)
    ##
    comments = models.TextField(max_length=1000, blank=True)
    
    def get_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    class Meta:
        db_table='Cadet'
    
    """
    The cadet model is used for these PT related functions as the cadet page view is not dealing with a specific PtScore we can call on
    This could, and possibly should(??) if feasible, be moved to the Grader model
    """
        
    def get_max_score(self, scores):
        max_score = 0
        for score in scores:
            if score.score > max_score:
                max_score = score.score
        return max_score
    
    #this function finds the highest grader key & value above a given value. meant for use with the two mile stat
    #may need some optimizing and error checking
    def lower_key_value(self, value, score_value_dict):
        try:
            return score_value_dict[value] #in case the value matches a key perfectly (usual case for pushups and situps)
        except KeyError:
            #to account for scores going over what we have in the dict keys
            if value < score_value_dict[min(score_value_dict)]:
                return '100'
            
            #where two mile score is calculated
            value_dict_stripped = score_value_dict
            value_dict_stripped = [x.replace(':', '') for x in score_value_dict]
            
            value = value.replace(':', '')
            for i in value_dict_stripped:
                if int(value) >= int(i):
                    if int(value) <= int(i) + 6:
                        i = i[:2] + ":" + i[2:]
                        return score_value_dict[i] #how to get this to return the next i value?
            return 0
            
                
    def get_score_value(self, value, score_value_dict):
        try:
            return score_value_dict[str(value)]
        #a key error is raised when a the function is asked to handle a two-mile score value format
        except KeyError:
            return self.lower_key_value(value, score_value_dict)
              
    #The two mile event part of this needs to be fixed
    def average_total_score(self, scores, event='scores'):
        avg_score = 0
        num_scores = len(scores)
        sum_scores = 0
        if event == 'scores':
            for score in scores:
                sum_scores = sum_scores + score.score
        if event == 'pushups':
            for score in scores:
                sum_scores = sum_scores + score.pushups
        if event == 'situps':
            for score in scores:
                sum_scores = sum_scores + score.situps
        if event == 'Two-mile run':
            for score in scores:
                concat_score = score.get_run_time_str().replace(':','')
                sum_scores = sum_scores + int(concat_score)
            avg_score = sum_scores/num_scores
            avg_score_time = str(avg_score)[:2] + ':' + str(avg_score)[2:]
            return avg_score_time
        avg_score = sum_scores/num_scores
        return avg_score
    
    #needs to be fixed to get two mile to round up instead of down
    def avg_event(self, scores, event_score_values, event='scores'):
        score_sum = 0
        if event == 'scores':
            for score in scores:
                score_sum = score_sum + self.get_score_value(score.score, event_score_values)
        if event == 'pushups':
            for score in scores:
                score_sum = score_sum + int(self.get_score_value(score.pushups, event_score_values))
        if event == 'situps':
            for score in scores:
                score_sum = score_sum + int(self.get_score_value(score.situps, event_score_values))
        if event == 'Two-mile run':
            for score in scores:
                score_sum = score_sum + int(self.get_score_value(score.get_run_time_str(), event_score_values))
        average = score_sum/len(scores)
        return average
        
    #needs to be modified to use avg_event instead of avg_total_scores
    def strongest_weakest_event(self, scores, pushup_score_values, situp_score_values, two_mile_score_values, strong_weak):
        print strong_weak
        min_or_max = "None"
        avg_pushups = self.average_total_score(scores, event='pushups')
        pushup_value = self.get_score_value(avg_pushups, pushup_score_values)
        
        avg_situps = self.average_total_score(scores, event='situps')
        situp_value = situp_score_values[str(avg_situps)]
        print situp_value
        
        avg_two_mile = self.average_total_score(scores, event='Two-mile run')
        two_mile_value = self.get_score_value(avg_two_mile, two_mile_score_values)
        print two_mile_value
        
        if strong_weak == "weak":
            min_or_max = min(pushup_value, situp_value, two_mile_value)
        elif strong_weak == 'strong':
            min_or_max = max(pushup_value, situp_value, two_mile_value)
        print "min max %s"%min_or_max
        if min_or_max == two_mile_value:
            return "Two Mile"
        elif min_or_max == pushup_value:
            return 'Pushups'
        elif min_or_max == situp_value:
            return 'Situps'



"""The Cadre class is the model for cadre in the batallion. It extends the Users model"""
class Cadre(Users):
    rank = models.CharField(max_length = 25)
    position = models.CharField(max_length = 75)
    
    
    class Meta:
        db_table='Cadre'
        
        
"""Each Platoon can only belong to one company."""
class Platoon(models.Model):
    name = models.CharField(max_length=15, default ="1st Platoon")
    company = models.ForeignKey(Company, db_index=False, related_name='company', blank=True, null=True)
    
    class Meta:
        db_table='Platoon'
    
    def __unicode__(self):
        if self.company:
            return str(self.company) + ": " + self.name
        else:
            return self.name
        
class MsLevel(models.Model):
    name = models.CharField(max_length=3,choices=MS_LEVEL_CHOICES, blank=False)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table='MsLevel'
