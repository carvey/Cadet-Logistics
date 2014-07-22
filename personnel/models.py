
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
    
        
    def get_max_score(self, scores):
        max_score = 0
        for score in scores:
            if score.score > max_score:
                max_score = score.score
        return max_score
    
    def get_min_score(self, scores):
        min_score = scores[0].score
        for score in scores:
            if score.score < min_score:
                min_score = score.score
        return min_score
    
    #this function finds the highest grader key & value above a given value. meant for use with the two mile stat
    #may need some optimizing and error checking    
            
                
    def get_score_value(self, value, score_value_dict, event='default'):
        if event == 'pushups' or event == 'situps' or event == 'default':
            if str(value) in score_value_dict:
                return score_value_dict[str(value)]
            else:
                if value < max(score_value_dict):
                    return '100'
                else:
                    return '0'
        
        if event == 'Two-mile run':
            stripped_score_value_dict = [int(x.replace(':', '')) for x in score_value_dict]
            stripped_value = int(value.replace(':', ''))
            if str(value) in score_value_dict:
                return score_value_dict[str(value)]
            else: #extra code to account for in between values goes here
                for key in stripped_score_value_dict:
                    if stripped_value < key:
                        if stripped_value > key-6:
                            unstripped_value = str(key)
                            unstripped_value = unstripped_value[:2] + ':' + unstripped_value[2:]
                            try:
                                return score_value_dict[unstripped_value]
                            except KeyError:
                                if key < max(stripped_score_value_dict):
                                    return '100'
                                else:
                                    return '0'
            if stripped_value > max(stripped_score_value_dict):
                return '100'
            else:
                return '0'
                
    
    def get_avg_pushups(self, scores):
        sum_pushups = 0
        length = len(scores)
        for score in scores:
            sum_pushups = sum_pushups + int(score.pushups)
        avg = sum_pushups/length
        return avg
    
    def get_avg_situps(self, scores):
        sum_situps = 0
        length = len(scores)
        for score in scores:
            sum_situps = sum_situps + int(score.situps)
        avg = sum_situps/length
        return avg
        
    #still getting over 60 seconds in some cases. Average isn't quite right
    def get_avg_two_mile(self, scores):
        sum_time = 0
        length = len(scores)
        for score in scores:
            stripped_score = score.get_run_time_str().replace(':', '')
            seconds = int(stripped_score[2:])
            seconds = str(seconds/float(60))
            stripped_score = float(stripped_score[:2] + '.' + seconds[2:])
            sum_time = sum_time + stripped_score
        avg = sum_time/float(length)
        decimal = str(avg).split('.')[1]
        decimal = str(int(decimal) * 60)
        avg = str(avg).split('.')[0] + ':' + str(decimal)[:2]
        return avg
    
    def get_avg_total_score(self, scores):
        sum_time = 0
        length = len(scores)
        for score in scores:
            sum_time = sum_time + int(score.score)
        avg = sum_time/length
        return avg
    


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
