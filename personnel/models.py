import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.functional import lazy

from dateutil import rrule

from personnel.managers import DefaultManager, CadetManager
from mixins import GroupingMixin



'''Static variables'''
ONE = 'one'
TWO = 'two'
THREE = 'three'
FOUR = 'four'
FIVE = 'five'
MS_LEVEL_CHOICES = (
    (ONE, 'MS1'),
    (TWO, 'MS2'),
    (THREE, 'MS3'),
    (FOUR, 'MS4'),
    (FIVE, 'MS5')
)
male = 'Male'
female = 'Female'
GENDER_CHOICES = (
    (male, 'Male'),
    (female, 'Female')
)

BLOOD_TYPES = (
        ("I am not 100% sure", "I am not 100% sure"),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
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

    def get_age(self, day=None):
        """
        Gets the cadets age from a reference point passed in through the "day" param. If no reference point is
        specified, the current date is used. This parameter allows a cadets age to be calculated from the date
         of a pt test, as opposed the current time.
        :param day: The past or future reference point to get the cadets age from.
        :return: The age of the cadet
        """
        ref_time = day or datetime.date.today()
        return ref_time.year - self.birth_date.year - ((ref_time.month, ref_time.day) < (self.birth_date.month, self.birth_date.day))

    def generate_username(self, email=None):
        """
        This method should handle generating unique usernames for all users
        Currently, this is done by using the first portion of the users email address

        If the instance being called on has no user.email available, then an email
        can be passed in the email argument
        EX:
            A user with email: myschoolemail@georgiasouthern.edu
            Would get a username: myschoolemail
        :return: a username string
        """
        if not email:
            return self.user.email.rpartition('@')[0]
        else:
            return email.rpartition('@')[0]

    class Meta:
        abstract = True

class Company(models.Model, GroupingMixin):
    """Company is the model for the companies in the batallion"""
    objects = DefaultManager()

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

    def assign(self, cadet):
        cadet.company = self
        cadet.platoon = None
        cadet.squad = None
        cadet.save()

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

    def get_staff_form(self):
        from forms import CompanyStaffForm
        form = CompanyStaffForm(initial={
            'commander': self.company_commander,
            'first_sgt': self.first_sergeant,
            'xo': self.executive_officer
        })
        return form


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
    _ms_level = models.ForeignKey('MsLevel', blank=False, null=False, related_name="cadets")

    commission_date = models.ForeignKey('Commission', blank=False, null=False, related_name="commission_date")

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
    blood_type = models.CharField(max_length=20, choices=BLOOD_TYPES, blank=False)
    car_model = models.CharField(max_length=100, blank=True, default="")
    car_tag = models.CharField(max_length=25, blank=True, default="")
    comments = models.TextField(max_length=1000, blank=True, default="")

    approved = models.BooleanField(default=True)

    objects = CadetManager()

    @property
    def ms_level(self):
        """
        This property should determine what a cadets MS level should be based on their commission date, and
        if necessary correct it to the proper MS level. This could be an expensive operation at times, but it
        does prevent any sort of manual updating of MS levels
        """
        graduation = self.commission_date.date
        today = datetime.date.today()
        ms_number = abs((graduation.year - 5) - today.year)
        ms_level = self._ms_level
        ms_level_number = int(ms_level.name.replace('MS', ''))
        if ms_number != ms_level_number:
            try:
                ms_level = MsLevel.objects.get(name="MS%s" % ms_number)
                self._ms_level = ms_level
                self.save()
            except:
                ms_level = MsLevel(name='MS')
        return ms_level

    #TODO this explanation could probably find a better home...
    """
    NOTE: Several methods are used here to access information regarding cadets and staff positions.
    Although there could be a staff position field for Cadet, which would eliminate the need for the is_staff()
    and get_staff_position() methods, it would also mean that anywhere in the system that allows for
    assignment information to be changed would have to implement methods that insured the cadet being moved
    out of the position had their staff_position field modified appropriately, and obviously the cadet being
    moved into the position would have to have their field updated appropriately. Although some logic needs to
    be done with this approach, just having these few methods saves from having to deal with the chaos that would
    be keeping up with a staff_position field
    """
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

    @staticmethod
    def get_staff_cadets():
        """
        This should return a queryset of all cadets who hold a staff position
        So I wrote this then realized I don't need it... but might come in handy sometime?
        :return: dict of the format {staff_position1__isnull: False, staff_position2__isnull: False, ...}
        """
        filter_dict = {}
        for position in Cadet.STAFF_POSITIONS.keys():
            filter_expression = "%s__isnull" % position
            filter_dict[filter_expression] = False

        class QOR(Q):
            default = Q.OR
        q_filter = QOR(**filter_dict)
        cadets = Cadet.objects.filter(q_filter)
        return cadets

    @staticmethod
    def get_avg_gpa(cadets):
        """
        function used to return the avg gpa of a set of cadets
        :param cadets:
        :return:
        """
        sum_gpa = 0
        cadets_with_gpa = 0
        for cadet in cadets:
            if cadet.gpa > 0:
                cadets_with_gpa += 1
                sum_gpa = sum_gpa + cadet.gpa
        if cadets_with_gpa:
            return round(sum_gpa / cadets_with_gpa, 2)
        else:
            return 0

    def set_squad(self, squad, commit=False):
        self.squad = squad
        self.platoon = squad.platoon
        self.company = squad.platoon.company
        if commit:
            self.save()

    def short_name(self):
        return "%s, %s." % (self.user.last_name, self.user.first_name[0])

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
    platoon_sergeant = models.OneToOneField('Cadet', db_index=False, related_name="platoon_sergeant",
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

    def company_short_name(self):
        return "%s %s%s" % (self.company.name[0], self.number, self.number_end_str())

    def get_sub_groupings(self):
        return self.squads.all()

    def assign(self, cadet):
        cadet.company = self.company
        cadet.platoon = self
        cadet.squad = None
        cadet.save()

    def set_platoon_leader(self, cadet):
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

    def get_squad_members(self):
        """
        Used instead of get_sub_cadets for populating the list of cadets in the organization chart
        minus the squad leader
        :return:
        """
        if self.squad_leader:
            return self.cadets.exclude(id__exact=self.squad_leader.id)

        return self.get_sub_cadets()

    def __unicode__(self):
        return self.get_name()

    def short_name(self):
        return "%s%s Squad" % (self.number, self.number_end_str())

    def assign(self, cadet):
        cadet.company = self.platoon.company
        cadet.platoon = self.platoon
        cadet.squad = self
        cadet.save()

    def set_squad_leader(self, cadet):
        """
        This method removes a cadet from squad leader, and replaces them with the cadet
        passed in as a parameter.
        :param cadet: the cadet to be set as the new platoon commander
        :return:
        """

        self.squad_leader = cadet
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

class Commission(models.Model):
    date = models.DateField()

    def __unicode__(self):
        return self.date.strftime("%B %Y")

class MsLevel(models.Model, GroupingMixin):
    """
    Model to represent each MS Level
    """
    objects = DefaultManager()

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


class Problems(models.Model):

    name = models.CharField(max_length=75, null=True)
    email = models.EmailField(null=True)
    problem = models.TextField(null=True)

    def __unicode__(self):
        return self.name