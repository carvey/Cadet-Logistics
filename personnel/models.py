
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
