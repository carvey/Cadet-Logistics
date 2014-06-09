from pt.models import PtScore

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

"""Users is the base class for Cadet and Cadre"""
class Users(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 30)
    age = models.PositiveIntegerField()
    
    def __str__(self):
        return (self.last_name + ", " + self.first_name)
    
    class Meta:
        abstract = True
        
"""Company is the model for the companies in the batallion"""
class Company(models.Model):
    name = models.CharField(max_length = 10, default = "", help_text="Enter Name of the new company here")
    commanding_officer = models.OneToOneField('Cadet', db_index=False, related_name='company_co', limit_choices_to={'is_company_staff':True}, blank=True, null=True, help_text="Enter the Name of the Commander Officer")
    first_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="company_firstsgt", limit_choices_to={'is_company_staff':True}, blank=True, null=True, help_text="Enter the First Sergeant for this Company")
    
    class Meta:
        db_table='Company'
    
    def __str__(self):
        return self.name

"""Cadet is the model for cadets in the batallion. This model extends the Users abstract model. Each cadet should ideally be assigned to a company"""
class Cadet(Users):
    company = models.ForeignKey(Company, blank=True, null=True)
    platoon = models.ForeignKey('Platoon', blank=True, null=True)
    ms_level = models.ForeignKey('MsLevel', blank=False, null=False)
    gpa = models.DecimalField(default=4.0, max_digits=3, decimal_places=2)
    ms_grade = models.IntegerField(default=100)
    is_staff = models.BooleanField(default = False)
    is_company_staff = models.BooleanField(default = False)
    '''@TODO Need to find a solution to filter the pt scores to show only those associated with the user'''
    #pt_scores = models.ForeignKey(PtScore, blank=True)
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
        return self.name
        
class MsLevel(models.Model):
    name = models.CharField(max_length=3,choices=MS_LEVEL_CHOICES, blank=False)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table='MsLevel'
