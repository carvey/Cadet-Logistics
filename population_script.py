from django.test import TestCase
from eagletrack.models import *
from pt.models import *
from attendance.models import *
import sys, datetime, os, random
sys.path.append(os.path.dirname(__file__))

# Create your tests here.

def populate():
    add_company(name="Alpha")
    add_company(name="Bravo")
    add_company(name="Charlie")
    add_company(name="Delta")
    
    alpha = Company.objects.get(name="Alpha")
    add_platoon(name="1st Platoon", company=alpha)
    add_platoon(name="2nd Platoon", company=alpha)
    
    bravo = Company.objects.get(name="Bravo")
    add_platoon(name="1st Platoon", company=bravo)
    add_platoon(name="2nd Platoon", company=bravo)
    
    charlie = Company.objects.get(name="Charlie")
    delta = Company.objects.get(name="Delta")
    
    #objects for for the platoons that were just created
    alpha1st = Platoon.objects.get(name="1st Platoon", company=alpha)
    alpha2nd = Platoon.objects.get(name="2nd Platoon", company=alpha)
    bravo1st = Platoon.objects.get(name="1st Platoon", company=bravo)
    bravo2nd = Platoon.objects.get(name="2nd Platoon", company=bravo)
    
    #adding ms levels
    add_mslevel(name="MS1")
    add_mslevel(name="MS2")
    add_mslevel(name="MS3")
    add_mslevel(name="MS4")
    
    #getting objects for the ms levels that were just created
    ms1 = MsLevel.objects.get(name="MS1")
    ms2 = MsLevel.objects.get(name="MS2")
    ms3 = MsLevel.objects.get(name="MS3")
    ms4 = MsLevel.objects.get(name="MS4")
      
    add_cadet(first_name="Taylor", last_name="Cooper", age=20, ms_level=ms3, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Jason", last_name="Canter", age=20, ms_level=ms3, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Eddie", last_name="Hanson", age=20, ms_level=ms3, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Ashley", last_name="Scott", age=20, ms_level=ms3, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Danial", last_name="Miller", age=20, ms_level=ms3, company=alpha, platoon=alpha1st)
    
    add_cadet(first_name="Oliver", last_name= "Paige", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Gordon", last_name= "Thomas", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Chris", last_name= "Danials", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Joshua", last_name= "Springer", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Eva", last_name="Lowry", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)  
    
    add_cadet(first_name="Kellie", last_name="Rogers", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    add_cadet(first_name="Trenton", last_name="Francis", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    add_cadet(first_name="Samantha", last_name="Roberts", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    add_cadet(first_name="Robert", last_name="Bacon", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    add_cadet(first_name="Samual", last_name="Gates", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    
    
    add_cadet(first_name="Thomas", last_name="Lee", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    add_cadet(first_name="Jennifer", last_name="Stone", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    add_cadet(first_name="Michael", last_name="Han", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    add_cadet(first_name="Kathy", last_name="Marino", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    add_cadet(first_name="James", last_name="Cooper", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    
   
    add_cadet(first_name="Mary", last_name="Jones", age=18, ms_level=ms1, company=charlie)
    add_cadet(first_name="Roger", last_name="Alan", age=18, ms_level=ms1, company=charlie)
    add_cadet(first_name="Pablo", last_name="Smith", age=18, ms_level=ms1, company=charlie)
    add_cadet(first_name="Garret", last_name="Timpson", age=18, ms_level=ms1, company=charlie)
    add_cadet(first_name="Julia", last_name="Anderson", age=18, ms_level=ms1, company=charlie)

    
    add_cadet(first_name="Joe", last_name="Taylor", age=18, ms_level=ms1, company=delta)
    add_cadet(first_name="Jim", last_name="Bob", age=18, ms_level=ms1, company=delta)
    add_cadet(first_name="Alan", last_name="Smith", age=18, ms_level=ms1, company=delta)
    add_cadet(first_name="Jane", last_name="West", age=18, ms_level=ms1, company=delta)
    add_cadet(first_name="Anne", last_name="Locke", age=18, ms_level=ms1, company=delta)
    
    add_pt_test(date=datetime.datetime.today() + datetime.timedelta(days=2), ms_lvl_4=False)
    add_pt_test(date=datetime.datetime.today() + datetime.timedelta(days=5), ms_lvl_4=False)
    add_pt_test(date=datetime.datetime.today() + datetime.timedelta(days=7), ms_lvl_4=True)
    
    create_pt_scores(20)
    assign_eagle_id()

def add_company(name, co=None, fs=None):
    company= Company.objects.get_or_create(name=name, company_commander=co, first_sergeant=fs)[0]
    return company

def add_platoon(name, company):
    platoon = Platoon.objects.get_or_create(name=name, company=company)
    return platoon

def add_cadet(first_name, last_name, age, ms_level, company, platoon=None, gpa=4.0, ms_grade=100, is_staff=False, is_company_staff=False):
    c = Cadet.objects.get_or_create(first_name=first_name, last_name=last_name, age=age, ms_level=ms_level, company=company, platoon=platoon,  gpa=gpa)[0]
    return c

def add_mslevel(name):
    ms = MsLevel.objects.get_or_create(name=name)
    return ms

def add_pt_test(date, ms_lvl_4):
    return PtTest.objects.get_or_create(date=date,MsLevelFour=ms_lvl_4)

def create_pt_scores(number):
    grader_list = Cadet.objects.filter(ms_level__name='MS4' and 'MS3')
    cadets = Cadet.objects.all()
    pt_tests = PtTest.objects.all()
    
    for num in range(1,number):
        score = PtScore.objects.get_or_create(grader=random.choice(grader_list), pt_test=random.choice(pt_tests), cadet=random.choice(cadets), pushups=random.randint(0,80), situps=random.randint(0,80), two_mile="%s:%s" % (random.randint(0,20), random.randint(0,59)))
        
def assign_eagle_id():
    cadets = Cadet.objects.all()
    starting_id = 900000000
    for cadet in cadets:
        cadet.eagle_id = starting_id
        starting_id = starting_id + 1
        

if __name__ == '__main__':
    print "Starting Eagletrack Population script..."
    os.environ['DJANGO_SETTINGS_MODULE'] = 'eagletrack_project.settings'
    from eagletrack.models import Cadet, Company, Platoon, MsLevel
    populate()
    print "Population script has ran successfully"
    
    