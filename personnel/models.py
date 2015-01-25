from django.core.validators import MaxValueValidator, MinValueValidator, validate_email
from django.db import models
from django.contrib.auth.hashers import make_password
from collections import OrderedDict
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
male = 'Male'
female = 'Female'
GENDER_CHOICES = (
    (male, 'Male'),
    (female, 'Female')
)



class School(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Demographic(models.Model):
    demographic = models.CharField(max_length=25)

    def __unicode__(self):
        return self.demographic


class Users(models.Model):
    """Company is the model for the companies in the batallion"""
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=30)
    # pass this value to the set_password function get it hashed
    password = models.CharField(max_length=128, blank=True, null=False)
    age = models.PositiveIntegerField(blank=False)
    email = models.EmailField(blank=True, validators=[validate_email])
    demographic = models.ForeignKey(Demographic, blank=True, null=True)

    def __unicode__(self):
        return self.last_name + ", " + self.first_name

    def set_password(self, raw_passwd):
        self.password = make_password(raw_passwd)

    class Meta:
        abstract = True


class Company(models.Model):
    """Company is the model for the companies in the batallion"""
    name = models.CharField(max_length=10, default="", help_text="Enter Name of the new company here")
    company_commander = models.OneToOneField('Cadet', db_index=False, related_name='ccs',
                                             limit_choices_to={'is_company_staff': True}, blank=True, null=True,
                                             help_text="Enter the Name of the Commander Officer")
    first_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="first_sgts",
                                          limit_choices_to={'is_company_staff': True}, blank=True, null=True,
                                          help_text="Enter the First Sergeant for this Company")

    class Meta:
        db_table = 'Company'

    def __unicode__(self):
        return self.name

    def set_first_sergeant(self, cadet):
        if self.first_sergeant:
            self.first_sergeant.is_company_staff = False

        self.first_sergeant = cadet
        cadet.is_company_staff = True
        cadet.save()
        self.save()

    def set_commander(self, cadet):
        if self.company_commander:
            self.company_commander.is_company_staff = False

        self.company_commander = cadet
        cadet.is_company_staff = True
        cadet.save()
        self.save()


class Cadet(Users):
    """Cadet is the model for cadets in the batallion.
    This model extends the Users abstract model. Each cadet should ideally be assigned to a company"""
    BLOOD_TYPES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B-'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    )

    eagle_id = models.PositiveIntegerField(default=0, blank=False, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False, null=True)
    school = models.ForeignKey(School, blank=True, null=True)

    # #
    company = models.ForeignKey(Company, blank=True, null=True)
    platoon = models.ForeignKey('Platoon', blank=True, null=True)
    ms_level = models.ForeignKey('MsLevel', blank=False, null=False)
    gpa = models.DecimalField(default=4.0, max_digits=3, decimal_places=2, blank=True)
    ms_grade = models.IntegerField(default=100, blank=True)
    is_staff = models.BooleanField(default=False)
    is_company_staff = models.BooleanField(default=False)
    # #
    cell_number = models.CharField(max_length=14, blank=True)
    #the volunteer_hours_completed field is a measure of the amount of hours completed
    volunteer_hours_completed = models.IntegerField(default=0, blank=True)
    #the volunteer_hours_status boolean is to tell whether a cadet has completed the minimum number of hours
    volunteer_hours_status = models.BooleanField(default=False)
    turned_in_104r = models.BooleanField(default=False)
    # #
    on_profile = models.BooleanField(default=False)
    profile_reason = models.CharField(max_length=250, blank=True)
    events_missed = models.PositiveIntegerField(default=0, blank=True)
    class_events_missed = models.PositiveIntegerField(default=0, blank=True)
    lab_events_missed = models.PositiveIntegerField(default=0, blank=True)
    pt_missed = models.PositiveIntegerField(default=0, blank=True)
    attendance_rate = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                  blank=True)  # logic for true and false attended is 100 and 0
    at_risk = models.BooleanField(default=False)
    # #
    contracted = models.BooleanField(default=False)
    smp = models.BooleanField(default=False)
    nurse = models.BooleanField(default=False)
    nurse_contracted = models.BooleanField(default=False)
    dropped = models.BooleanField(default=False)
    commissioned = models.BooleanField(default=False)
    # #
    ranger_challenge = models.BooleanField(default=False)
    color_guard = models.BooleanField(default=False)

    # #
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPES, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_tag = models.CharField(max_length=25, blank=True)
    comments = models.TextField(max_length=1000, blank=True)

    def get_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    #function used to return the avg gpa of a set of cadets
    @staticmethod
    def get_avg_gpa(cadets):
        sum_gpa = 0
        cadets_with_gpa = 0
        for cadet in cadets:
            if cadet.gpa > 0:
                cadets_with_gpa += 1
                sum_gpa = sum_gpa + cadet.gpa
        return round(sum_gpa / cadets_with_gpa, 2)

    @staticmethod
    def get_top_gpa_cadets(cadets, num=3):
        gpas = {}
        for cadet in cadets:
            gpas.update({cadet.gpa: cadet})
        gpas = OrderedDict(reversed(sorted(gpas.items(), key=lambda t: t[0])))
        top_gpas = OrderedDict()
        count = 0
        for x, y in gpas.items():
            top_gpas.update({x: y})
            count += 1
            if count == num:
                break
        return reversed(sorted(top_gpas.items()))

    class Meta:
        db_table = 'Cadet'


class Cadre(Users):
    """The Cadre class is the model for cadre in the batallion. It extends the Users model"""
    rank = models.CharField(max_length=25)
    position = models.CharField(max_length=75)

    class Meta:
        db_table = 'Cadre'


class Platoon(models.Model):
    """Each Platoon can only belong to one company."""
    name = models.PositiveIntegerField(default=1, blank=False)
    company = models.ForeignKey(Company, db_index=False, related_name='company', blank=True, null=True)
    platoon_commander = models.OneToOneField('Cadet', db_index=False, related_name='pc',
                                             limit_choices_to={'is_company_staff': True}, blank=True, null=True,
                                             help_text="Enter the Platoon Commander")
    platoon_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="ps",
                                          limit_choices_to={'is_company_staff': True}, blank=True, null=True,
                                          help_text="Enter the Platoon Sergeant")

    class Meta:
        db_table = 'Platoon'

    def __unicode__(self):
        end_string = "th"
        if self.name % 10 == 1:
            end_string = "st"
        elif self.name % 10 == 2:
            end_string = "nd"
        elif self.name % 10 == 3:
            end_string = "rd"

        if self.company:
            return str(self.company) + " Company, " + str(self.name) + end_string + " Platoon"
        else:
            return str(self.name) + end_string + " Platoon"

    def display_name(self):
        end_string = "th"
        if self.name % 10 == 1:
            end_string = "st"
        elif self.name % 10 == 2:
            end_string = "nd"
        elif self.name % 10 == 3:
            end_string = "rd"
        return str(self.name) + end_string + " Platoon"

    def set_platoon_commander(self, cadet):
        if self.platoon_commander:
            self.platoon_commander.is_company_staff = False

        self.platoon_commander = cadet
        cadet.is_company_staff = True
        cadet.save()
        self.save()

    def set_platoon_sergeant(self, cadet):
        if self.platoon_sergeant:
            self.platoon_sergeant.is_company_staff = False

        self.platoon_sergeant = cadet
        cadet.is_company_staff = True
        cadet.save()
        self.save()


class MsLevel(models.Model):
    name = models.CharField(max_length=3, choices=MS_LEVEL_CHOICES, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'MsLevel'


class Year(models.Model):
    year = models.CharField(max_length=9, blank=False, default="2014-2015")


class SnapShot(models.Model):
    """This model is meant to record data at certain time intervals.
    All data should be filtered to active cadets.
    Time interval: 3 times per semester (max)"""

    #auto_now_add will need to be true at deployment unless we want to specify date manually
    date = models.DateField(auto_now_add=False)
    year = models.ForeignKey(Year, null=True)
    cadets = models.PositiveIntegerField(default=0)
    males = models.PositiveIntegerField(default=0)
    females = models.PositiveIntegerField(default=0)
    contracted_cadets = models.PositiveIntegerField(default=0)
    smp_cadets = models.PositiveIntegerField(default=0)

    ms1_count = models.PositiveIntegerField(default=0)
    ms2_count = models.PositiveIntegerField(default=0)
    ms3_count = models.PositiveIntegerField(default=0)
    ms4_count = models.PositiveIntegerField(default=0)

    avg_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True)
    avg_ms1_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True)
    avg_ms2_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True)
    avg_ms3_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True)
    avg_ms4_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True)

    def __unicode__(self):
        return self.date.strftime('%m %Y, %d')