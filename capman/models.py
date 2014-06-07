from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 30)
    age = models.IntegerField()
    
    def __str__(self):
        return (self.last_name + ", " + self.first_name)
    
    class Meta:
        abstract = True
    
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
    ms_level = models.CharField(max_length = 4,
                                choices = ms_level_choices,
                                default = one)
    is_staff = models.BooleanField(default = False)
    is_company_staff = models.BooleanField(default = False)

    class Meta:
        db_table='Cadet'
        
class Cadre(Users):
    rank = models.CharField(max_length = 25)
    position = models.CharField(max_length = 75)

    class Meta:
        db_table='Cadre'