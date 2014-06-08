from django.db import models
from django.contrib.auth.models import User

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
    platoons = models.ForeignKey('Platoon', db_index=False, related_name='company_platoons', blank=True, null=True)
    
    class Meta:
        db_table='Company'
    
    def __str__(self):
        return self.name

"""Cadet is the model for cadets in the batallion. This model extends the Users abstract model. Each cadet should ideally be assigned to a company"""
class Cadet(Users):
    one = 'one'
    two = 'two'
    three = 'three'
    four = 'four'
    ms_level_choices = (
                (one, 'MS1'),
                (two, 'MS2'),
                (three, 'MS3'),
                (four, 'MS4'),
                )
    company = models.OneToOneField(Company, blank=True, null=True)
    ms_level = models.CharField(max_length = 4,
                                choices = ms_level_choices,
                                default = one)
    gpa = models.DecimalField(default=4.0, max_digits=3, decimal_places=2)
    ms_grade = models.IntegerField(default=100)
    is_staff = models.BooleanField(default = False)
    is_company_staff = models.BooleanField(default = False)
    class Meta:
        db_table='Cadet'

"""The Cadre class is the model for cadre in the batallion"""
class Cadre(Users):
    rank = models.CharField(max_length = 25)
    position = models.CharField(max_length = 75)
    class Meta:
        db_table='Cadre'

class Platoon(Company):
    pass