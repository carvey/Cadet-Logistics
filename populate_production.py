import os

from personnel.models import *
from pt.models import *
from pt.constants import *
from pt.pt_utils.utils import create_graders


def populate():

    print "Creating companies"
    alpha = add_company(name="Alpha")
    bravo = add_company(name="Bravo")
    charlie = add_company(name="Charlie")
    delta = add_company(name="Delta")
    staff = add_company(name="Staff")
    print "done creating companies"
    print "-----------------------"

    print "creating platoons and squads"

    """
    Naming Scheme:
        Platoons: company name + platoon number
        Squads:  company name + platoon number + squad number
    """
    alpha1st = add_platoon(number=1, company=alpha)
    alpha11 = add_squad(number=1, platoon=alpha1st)
    alpha12 = add_squad(number=2, platoon=alpha1st)
    alpha13 = add_squad(number=3, platoon=alpha1st)
    alpha14 = add_squad(number=4, platoon=alpha1st)

    bravo1st = add_platoon(number=1, company=bravo)
    bravo11 = add_squad(number=1, platoon=bravo1st)
    bravo12 = add_squad(number=2, platoon=bravo1st)
    bravo13 = add_squad(number=3, platoon=bravo1st)
    bravo14 = add_squad(number=4, platoon=bravo1st)
    bravo2nd = add_platoon(number=2, company=bravo)
    bravo21 = add_squad(number=1, platoon=bravo2nd)
    bravo22 = add_squad(number=2, platoon=bravo2nd)
    bravo23 = add_squad(number=3, platoon=bravo2nd)
    bravo24 = add_squad(number=4, platoon=bravo2nd)

    charlie1st = add_platoon(number=1, company=charlie)
    charlie11 = add_squad(number=1, platoon=charlie1st)
    charlie12 = add_squad(number=2, platoon=charlie1st)
    charlie13 = add_squad(number=3, platoon=charlie1st)
    charlie14 = add_squad(number=4, platoon=charlie1st)
    charlie2nd = add_platoon(number=2, company=charlie)
    charlie21 = add_squad(number=1, platoon=charlie2nd)
    charlie22 = add_squad(number=2, platoon=charlie2nd)
    charlie23 = add_squad(number=3, platoon=charlie2nd)
    charlie24 = add_squad(number=4, platoon=charlie2nd)

    delta1st = add_platoon(number=1, company=delta)
    delta11 = add_squad(number=1, platoon=delta1st)
    delta12 = add_squad(number=2, platoon=delta1st)
    delta13 = add_squad(number=3, platoon=delta1st)
    delta14 = add_squad(number=4, platoon=delta1st)

    staff1st = add_platoon(number=1, company=staff)
    staff11 = add_squad(number=1, platoon=staff1st)

    print "done creating platoons and squads"
    print "-----------------------"

    print "adding ms levels"
    # adding ms levels
    ms1 = add_mslevel(name="MS1")
    ms2 = add_mslevel(name="MS2")
    ms3 = add_mslevel(name="MS3")
    ms4 = add_mslevel(name="MS4")
    ms4 = add_mslevel(name="MS5")
    print "done adding ms levels"
    print "-----------------------"

    print "Adding demographics"
    add_demographic(demographic="White")
    add_demographic(demographic="Black")
    add_demographic(demographic="Asian")
    add_demographic(demographic="Native American")
    add_demographic(demographic="Hispanic")
    add_demographic(demographic="Other")
    print "done adding demographics"
    print "-----------------------"

    print "Creating graders"
    create_graders()
    print "Done creating Graders"
    print "-----------------------"


def add_company(name, co=None, fs=None):
    company = Company.objects.get_or_create(name=name, company_commander=co, first_sergeant=fs)[0]
    return company


def add_platoon(number, company):
    platoon = Platoon.objects.get_or_create(number=number, company=company)[0]
    return platoon


def add_squad(number, platoon):
    squad = Squad.objects.get_or_create(number=number, platoon=platoon)[0]
    return squad


def add_mslevel(name):
    ms = MsLevel.objects.get_or_create(name=name)[0]
    return ms


def add_pt_test(date, ms_classes, record=False):
    pt_test = PtTest.objects.get_or_create(date=date, record=record)[0]
    for ms_level in ms_classes:
        pt_test.ms_levels.add(ms_level)
    return pt_test


def add_demographic(demographic):
    demo = Demographic.objects.get_or_create(demographic=demographic)
    return demo


def run_production_population():
    print "Starting Eagletrack Production Population script..."

    # import django
    # django.setup()

    populate()
    print "Population script has ran successfully"