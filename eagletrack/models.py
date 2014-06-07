from django.db import models
from django.contrib.auth.models import User

'''Users is the base class for Cadet and Cadre'''
class Users(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 30)
    age = models.PositiveIntegerField()
    
    def __str__(self):
        return (self.last_name + ", " + self.first_name)
    
    class Meta:
        abstract = True
        
class Company(models.Model):
    ALPHA = 'alpha'
    BRAVO = 'bravo'
    CHARLIE = 'charlie'
    DELTA = 'delta'
    
    COMPANY_NAMES = (
        (ALPHA, 'alpha'),
        (BRAVO, 'bravo'),
        (CHARLIE, 'charlie'),
        (DELTA, 'delta')             
        )
    name = models.CharField(max_length = 2, choices = COMPANY_NAMES, default = ALPHA)
    co = models.OneToOneField('Cadet', related_name='Company')
    platoons = models.OneToManyField('Platoon', related_name='Company')
    
    class Meta:
        db_table='Company'
    
    def __str__(self):
        return self.name
    
class Cadet(Users):
    def __init__(self):
        pass
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
    company = models.OneToOneField(Company)
    ms_level = models.CharField(max_length = 4,
                                choices = ms_level_choices,
                                default = one)
    gpa = models.IntegerField()
    ms_grade = models.IntegerField()
    is_staff = models.BooleanField(default = False)
    is_company_staff = models.BooleanField(default = False)
    class Meta:
        db_table='Cadet'
        
class Cadre(Users):
    rank = models.CharField(max_length = 25)
    position = models.CharField(max_length = 75)

    class Meta:
        db_table='Cadre'

class Platoon(models.Model):
    pass