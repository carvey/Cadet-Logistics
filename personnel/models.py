# from dateutil.relativedelta import relativedelta
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, validate_email
from django.db import models
from django.contrib.auth.hashers import make_password
from collections import OrderedDict
from django.contrib.auth.models import AbstractUser, User
from django.core.urlresolvers import reverse

from personnel.managers import SearchManager
from mixins import GroupingMixin


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

# The functionality to use this class is not yet implemented
class School(models.Model):
    """
    The School that a cadet attends
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Demographic(models.Model):
    """
    To be used for tracking cadet demographics
    """
    demographic = models.CharField(max_length=25)

    def __unicode__(self):
        return self.demographic

    @staticmethod
    def to_list():
        """
        Gets a list of all the demographics, and compiles them into a list
        :return: A list of all demographics
        """
        #The vallues_list() method on the queryset will return a list of tuples like: (id, demo)
        demo_list = Demographic.objects.all().values_list()
        #The second value (the demographic) is what we need
        return [(demo[1], demo[1]) for demo in demo_list]


class Users(models.Model):
    """Company is the model for the companies in the batallion"""
    user = models.OneToOneField(User)
    # age = models.PositiveIntegerField(blank=False, null=True, default=18)
    birth_date = models.DateField(blank=False, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False, default='male')
    demographic = models.ForeignKey(Demographic, blank=True, null=True)

    def __unicode__(self):
        return self.user.last_name + ", " + self.user.first_name

    def get_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def get_age(self):
        today = datetime.date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    class Meta:
        abstract = True


# class Grouping(models.Model):
#
#     def blah(self):
#         raise NotImplementedError
#
#     class Meta:
#         abstract = True




class Company(models.Model, GroupingMixin):
    """Company is the model for the companies in the batallion"""
    objects = SearchManager()

    name = models.CharField(max_length=10, default="", help_text="Enter Name of the new company here")
    company_commander = models.OneToOneField('Cadet', db_index=False, related_name='company_commander',
                                             blank=True, null=True, help_text="Enter the Name of the Commander Officer")
    first_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="first_sgt",
                                          blank=True, null=True, help_text="Enter the First Sergeant for this Company")
    executive_officer = models.OneToOneField('Cadet', db_index=False, related_name="xo",
                                             blank=True, null=True, help_text="Enter the XO for this Company")

    class Meta:
        db_table = 'Company'

    def __unicode__(self):
        return self.name

    def get_name(self):
        return "%s Company" % self.name

    def short_name(self):
        return self.get_name()

    def get_sub_groupings(self):
        return self.platoons.all()


    def set_first_sergeant(self, cadet):
        """
        This method sets the company First Sergeant position to the cadet passed in as the cadet arg
        :param cadet: the cadet to be set as the new first sergeant
        :return:
        """
        self.first_sergeant = cadet
        self.save()

    def set_commander(self, cadet):
        """
        This method sets the company CO position to the cadet passed in as the cadet arg
        :param cadet: the cadet to be set as the new company commander
        :return:
        """
        self.company_commander = cadet
        self.save()

    def set_executive_officer(self, cadet):
        """
        This method sets the company XO position to the cadet passed in as the cadet arg
        :param cadet: the cadet to be set as the new company commander
        :return:
        """
        self.executive_officer = cadet
        self.save()

    def get_initial(self):
        return self.name[0]

    def count(self):
        return self.cadets.all().count()

    def get_link(self):
        return '/personnel/companies/%s' % self.id

    def get_co(self):
        return {
            'title': "Company Commander",
            "cadet": self.company_commander
        }

    def get_sgt(self):
        return {
            'title': "First Sergeant",
            'cadet': self.first_sergeant
        }


class Cadet(Users):
    """
    Cadet is the model for cadets in the batallion.
    This model extends the Users abstract model. Each cadet should ideally be assigned to a company, platoon, and squad
    """

    """
    This is a dict of related_name's (keys) of all the current possible staff positions a cadet can have, as well their
    more readable name (values). Register the related_names in this list for the Cadet model helper methods to iterate through
    """
    STAFF_POSITIONS = {'company_commander': 'Company Commander', 'first_sgt': 'First Sergeant',
                       'platoon_commander': 'Platoon Commander', 'platoon_sergeant': 'Platoon Sergeant',
                       'squad_leader': 'Squad Leader'}

    eagle_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    school = models.ForeignKey(School, blank=True, null=True)

    # #
    company = models.ForeignKey(Company, blank=True, null=True, related_name="cadets")
    platoon = models.ForeignKey('Platoon', blank=True, null=True, related_name="cadets")
    squad = models.ForeignKey('Squad', blank=True, null=True, related_name="cadets")
    ms_level = models.ForeignKey('MsLevel', blank=False, null=False, related_name="cadets")
    gpa = models.DecimalField(default=4.0, max_digits=3, decimal_places=2, blank=True, null=True)
    ms_grade = models.IntegerField(default=100, blank=True, null=True)
    # #
    cell_number = models.CharField(max_length=14, blank=False)
    #the volunteer_hours_count field is a measure of the amount of hours completed
    volunteer_hours_count = models.IntegerField(default=0, blank=True, null=True)
    #the volunteer_hours_completed boolean is to tell whether a cadet has completed the minimum number of hours
    volunteer_hours_completed = models.BooleanField(default=False)
    turned_in_104r = models.BooleanField(default=False)
    # #
    #TODO consider a profile model in the pt app instead of this field?
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

    objects = SearchManager()

    def is_staff(self):
        """
        Determines whether or not a cadet is assigned to a staff position or not
        :return: A boolean determining whether or not the cadet instance is assigned to a staff position
        """
        for staff_position in self.STAFF_POSITIONS:
            if hasattr(self, staff_position):
                return True
        return False

    def get_staff_position(self):
        """
        Returns a string representation of the staff position that a cadet is assigned to
        :return: The staff position that the cadet is assigned to, or False if they are not assigned to a position
        """
        for staff_position in self.STAFF_POSITIONS:
            if hasattr(self, staff_position):
                return "%s %s" % (self.__dict__["_%s_cache" % staff_position], self.STAFF_POSITIONS[staff_position])
        return False


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
    ms_level_assignment = models.ForeignKey('MsLevel', related_name='instructors', blank=True, null=True)

    class Meta:
        db_table = 'Cadre'


class Platoon(models.Model, GroupingMixin):
    """Each Platoon can only belong to one company."""
    number = models.PositiveIntegerField(default=1, blank=False)
    company = models.ForeignKey(Company, db_index=False, related_name='platoons', blank=True, null=True)
    platoon_commander = models.OneToOneField('Cadet', db_index=False, related_name='platoon_commander',
                                             blank=True, null=True, help_text="Enter the Platoon Commander")
    platoon_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="platoon_sgt",
                                            blank=True, null=True, help_text="Enter the Platoon Sergeant")

    class Meta:
        db_table = 'Platoon'

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        if self.company:
            return str(self.company) + " Company, " + str(self.number) + self.number_end_str() + " Platoon"
        else:
            return str(self.number) + self.number_end_str() + " Platoon"

    def short_name(self):
        return str(self.number) + self.number_end_str() + " Platoon"

    def get_sub_groupings(self):
        return self.squads.all()


    def set_platoon_commander(self, cadet):
        """
        This method removes a cadet from platoon commander, and replaces them with the cadet
        passed in as a parameter.
        :param cadet: the cadet to be set as the new platoon commander
        :return:
        """
        self.platoon_commander = cadet
        cadet.save()
        self.save()

    def set_platoon_sergeant(self, cadet):
        """
        This method removes a cadet from platoon sergeant, and replaces them with the cadet
        passed in as a parameter.
        :param cadet: the cadet to be set as the new platoon sergeant
        :return:
        """
        self.platoon_sergeant = cadet
        cadet.save()
        self.save()

    def count(self):
        return len(self.cadets.all())

    def get_link(self):
        return '/personnel/platoons/%s' % self.id

    def get_co(self):
        return {
            'title': "Platoon Leader",
            'cadet': self.platoon_commander
        }

    def get_sgt(self):
        return {
            'title': "Platoon Sergeant",
            'cadet': self.platoon_sergeant
        }


class Squad(models.Model, GroupingMixin):
    number = models.PositiveSmallIntegerField(blank=False)
    platoon = models.ForeignKey(Platoon, related_name='squads', blank=False)
    squad_leader = models.OneToOneField(Cadet, db_index=False, related_name="squad_leader",
                                        blank=True, null=True,
                                        help_text="Enter the Squad Leader")

    def get_name(self):
        if self.platoon:
            return str(self.platoon) + ", " + str(self.number) + self.number_end_str() + " Squad"
        else:
            return str(self.number) + self.number_end_str() + " Squad"


    def get_sub_groupings(self):
        return None

    def __unicode__(self):
        return self.get_name()

    def short_name(self):
        return "%s%s Squad" % (self.number, self.number_end_str())

    def set_squad_leader(self, cadet):
        """
        This method removes a cadet from squad leader, and replaces them with the cadet
        passed in as a parameter.
        :param cadet: the cadet to be set as the new platoon commander
        :return:
        """

        self.squad_leader = cadet
        cadet.save()
        self.save()

    def count(self):
        return len(self.cadets.all())

    def get_link(self):
        return '/personnel/squads/%s' % self.id

    def get_co(self):
        return None

    def get_sgt(self):
        return {
            "title": "Squad Leader",
            "cadet": self.squad_leader
        }


# TODO: Needs to be added to GroupingMixin
class MsLevel(models.Model, GroupingMixin):
    """
    Model to represent each MS Level
    """
    objects = SearchManager()

    name = models.CharField(max_length=3, choices=MS_LEVEL_CHOICES, blank=False)

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        return "%s Class" % self.name

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