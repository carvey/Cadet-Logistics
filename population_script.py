import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'eagletrack_project.settings'

from django.test import TestCase
from personnel.models import *
from pt.models import *
from pt.constants import *
from attendance.models import *
import sys, datetime, random

sys.path.append(os.path.dirname(__file__))

# Create your tests here.
cadets = Cadet.objects.all()

def clear_cadets():
    for cadet in Cadet.objects.all():
        cadet.delete()


def populate():
    #use this for when snapshots need testing, otherwise comment it out
    clear_cadets()

    add_company(name="Alpha")
    add_company(name="Bravo")
    add_company(name="Charlie")
    add_company(name="Delta")

    alpha = Company.objects.get(name="Alpha")
    add_platoon(name=1, company=alpha)
    add_platoon(name=2, company=alpha)

    bravo = Company.objects.get(name="Bravo")
    add_platoon(name=1, company=bravo)
    add_platoon(name=2, company=bravo)

    charlie = Company.objects.get(name="Charlie")
    add_platoon(name=1, company=charlie)
    add_platoon(name=2, company=charlie)

    delta = Company.objects.get(name="Delta")
    add_platoon(name=1, company=delta)
    add_platoon(name=2, company=delta)

    # objects for for the platoons that were just created
    alpha1st = Platoon.objects.get(name=1, company=alpha)
    alpha2nd = Platoon.objects.get(name=2, company=alpha)
    bravo1st = Platoon.objects.get(name=1, company=bravo)
    bravo2nd = Platoon.objects.get(name=2, company=bravo)
    charlie1st = Platoon.objects.get(name=1, company=charlie)
    charlie2nd = Platoon.objects.get(name=2, company=charlie)
    delta1st = Platoon.objects.get(name=1, company=delta)
    delta2nd = Platoon.objects.get(name=2, company=delta)

    # adding ms levels
    add_mslevel(name="MS1")
    add_mslevel(name="MS2")
    add_mslevel(name="MS3")
    add_mslevel(name="MS4")

    # getting objects for the ms levels that were just created
    ms1 = MsLevel.objects.get(name="MS1")
    ms2 = MsLevel.objects.get(name="MS2")
    ms3 = MsLevel.objects.get(name="MS3")
    ms4 = MsLevel.objects.get(name="MS4")

    add_demographic(demographic="White")
    add_demographic(demographic="Black")
    add_demographic(demographic="Asian")
    add_demographic(demographic="American Indian")
    add_demographic(demographic="Hispanic")

    add_cadet(first_name="Taylor", last_name="Cooper", age=20, ms_level=ms4, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Jason", last_name="Canter", age=20, ms_level=ms4, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Eddie", last_name="Hanson", age=20, ms_level=ms4, company=alpha, platoon=alpha1st)
    add_cadet(first_name="Ashley", last_name="Scott", age=20, gender="Female", ms_level=ms4, company=alpha,
              platoon=alpha1st)
    add_cadet(first_name="Danial", last_name="Miller", age=20, ms_level=ms3, company=alpha, platoon=alpha1st)


    add_cadet(first_name="Oliver", last_name="Paige", age=20, gender="Female", ms_level=ms3, company=alpha,
              platoon=alpha2nd)
    add_cadet(first_name="Gordon", last_name="Thomas", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Chris", last_name="Danials", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Joshua", last_name="Springer", age=20, ms_level=ms3, company=alpha, platoon=alpha2nd)
    add_cadet(first_name="Eva", last_name="Lowry", age=20, gender="Female", ms_level=ms3, company=alpha,
              platoon=alpha2nd)


    add_cadet(first_name="Kellie", last_name="Rogers", age=19, gender="Female", ms_level=ms2, company=bravo,
              platoon=bravo1st)
    add_cadet(first_name="Trenton", last_name="Francis", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    add_cadet(first_name="Samantha", last_name="Roberts", age=19, gender="Female", ms_level=ms2, company=bravo,
              platoon=bravo1st)
    add_cadet(first_name="Robert", last_name="Bacon", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)
    add_cadet(first_name="Samual", last_name="Gates", age=19, ms_level=ms2, company=bravo, platoon=bravo1st)


    add_cadet(first_name="Thomas", last_name="Lee", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    add_cadet(first_name="Jennifer", last_name="Stone", age=19, gender="Female", ms_level=ms2, company=bravo,
              platoon=bravo2nd)
    add_cadet(first_name="Michael", last_name="Han", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)
    add_cadet(first_name="Kathy", last_name="Marino", age=19, gender="Female", ms_level=ms2, company=bravo,
              platoon=bravo2nd)
    add_cadet(first_name="James", last_name="Cooper", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd)



    add_cadet(first_name="Mary", last_name="Jones", age=18, gender="Female", ms_level=ms1, company=charlie, platoon=charlie1st)
    add_cadet(first_name="Roger", last_name="Alan", age=18, ms_level=ms1, company=charlie, platoon=charlie1st)
    add_cadet(first_name="Pablo", last_name="Smith", age=18, ms_level=ms1, company=charlie, platoon=charlie1st)
    add_cadet(first_name="Garret", last_name="Timpson", age=18, ms_level=ms1, company=charlie, platoon=charlie2nd)
    add_cadet(first_name="Julia", last_name="Anderson", age=18, gender="Female", ms_level=ms1, company=charlie, platoon=charlie2nd)



    add_cadet(first_name="Joe", last_name="Taylor", age=18, ms_level=ms1, company=delta, platoon=delta1st)
    add_cadet(first_name="Jim", last_name="Bob", age=18, ms_level=ms1, company=delta, platoon=delta1st)
    add_cadet(first_name="Alan", last_name="Smith", age=18, ms_level=ms1, company=delta, platoon=delta2nd)
    add_cadet(first_name="Jane", last_name="West", age=18, gender="Female", ms_level=ms1, company=delta, platoon=delta2nd)
    add_cadet(first_name="Anne", last_name="Locke", age=18, gender="Female", ms_level=ms1, company=delta, platoon=delta2nd)



    add_pt_test(date=datetime.date(2014, 6, 1) + datetime.timedelta(days=2), ms_lvl_4=False)
    add_pt_test(date=datetime.date(2014, 6, 1) + datetime.timedelta(days=5), ms_lvl_4=False)
    add_pt_test(date=datetime.date(2014, 6, 1) + datetime.timedelta(days=7), ms_lvl_4=True)

    create_pt_scores()
    assign_eagle_id()
    assign_cell_num()
    assign_email()
    assign_gpa()
    assign_ms_grade()
    assign_contract_smp()
    assign_gender_to_males()
    generate_volunteer_completion()
    assign_nursing_cadets()
    assign_demographics()
    assign_at_risk_cadets()
    generate_profiles()

    generate_snapshots(date = datetime.date(2014, 6, 1), start=0, end=0)
    generate_snapshots(date = datetime.date(2014, 7, 1), start=0, end=3)
    generate_snapshots(date = datetime.date(2014, 8, 1), start=0, end=12)
    generate_snapshots(date = datetime.date(2014, 9, 1), start=0, end=15)
    generate_snapshots(date = datetime.date(2014, 10, 1), start=0, end=23)
    generate_snapshots(date = datetime.date(2014, 11, 1), start=0, end=21)
    generate_snapshots(date = datetime.date(2014, 12, 1), start=0, end=30)

    create_graders()
    #generate_pt_score_value()


def add_company(name, co=None, fs=None):
    company = Company.objects.get_or_create(name=name, company_commander=co, first_sergeant=fs)[0]
    return company


def add_platoon(name, company):
    platoon = Platoon.objects.get_or_create(name=name, company=company)
    return platoon


def add_cadet(first_name, last_name, age, ms_level, company, gender="Male", platoon=None, ms_grade=100, is_staff=False,
              is_company_staff=False):
    c = Cadet.objects.get_or_create(first_name=first_name, last_name=last_name, age=age, gender=gender,
                                    ms_level=ms_level,
                                    company=company, platoon=platoon)[0]
    return c


def add_mslevel(name):
    ms = MsLevel.objects.get_or_create(name=name)
    return ms


def add_pt_test(date, ms_lvl_4):
    pt_test = PtTest.objects.get_or_create(date=date, MsLevelFour=ms_lvl_4)
    return pt_test

def add_demographic(demographic):
    demo = Demographic.objects.get_or_create(demographic=demographic)
    return demo

def create_pt_scores():
    grader_list = Cadet.objects.filter(ms_level__name='MS4' and 'MS3')
    pt_tests = PtTest.objects.all()
    for test in pt_tests:
        for cadet in cadets:
            cadet_score = None
            try:
                cadet_score = PtScore.objects.get(cadet=cadet, pt_test=test) #checks to see whether a ptscore has already been created for this test and cadet
                cadet_score.save()
            except:
                pass
            if cadet_score == None:
                score = PtScore.objects.get_or_create(grader=random.choice(grader_list), pt_test=test, cadet=cadet, pushups=random.randint(0,80), situps=random.randint(0,80), score=0, two_mile="%s:%s" % (random.randint(12,20), random.randint(0,59)))
                score[0].save()


def generate_pt_score_value():
    pt_tests = PtTest.objects.all()
    score_values = Grader.objects.all()
    for test in pt_tests:
        pt_scores = PtScore.objects.filter(pt_test=test)
        for score in pt_scores:
            age = score.cadet.get_score_value_age_group(score.cadet, score_values)
            pushup_score_values = Grader.objects.get(gender=score.cadet.gender, activity='pushups',
                                                     age_group=age).get_ordered_dict()
            situp_score_values = Grader.objects.get(gender=score.cadet.gender, activity='situps',
                                                    age_group=age).get_ordered_dict()
            two_mile_score_values = Grader.objects.get(gender=score.cadet.gender, activity='Two-mile run',
                                                       age_group=age).get_ordered_dict()

            pushup_score = score.cadet.get_score_value(score.pushups, pushup_score_values)
            situp_score = score.cadet.get_score_value(score.situps, situp_score_values)
            two_mile_score = score.cadet.get_score_value(score.two_mile, two_mile_score_values)
            score.score = int(pushup_score) + int(situp_score) + int(two_mile_score)
            score.save()


def assign_eagle_id():
    starting_id = 900000000
    for cadet in cadets:
        cadet.eagle_id = starting_id
        starting_id += 1
        cadet.save()


def assign_cell_num():
    starting_num = 7702501639
    for cadet in cadets:
        cadet.cell_number = starting_num
        starting_num += 4
        cadet.save()


def assign_email():
    starting_num = 00000
    for cadet in cadets:
        cadet.email = cadet.first_name[:1].lower() + cadet.last_name.lower() + str(starting_num) + '@georgiasouthern.edu'
        starting_num += 75
        cadet.save()


def assign_gpa():
    for cadet in cadets:
        cadet.gpa = random.random() * 4
        cadet.save()


def assign_ms_grade():
    for cadet in cadets:
        cadet.ms_grade = random.randint(50, 100)
        cadet.save()


def assign_contract_smp():
    for cadet in cadets:
        rand = random.randint(0, 20)
        if rand % 6 == 0:
            cadet.contracted = True
        if rand % 4 == 0:
            cadet.smp = True
        cadet.save()


def generate_volunteer_completion():
    for cadet in cadets:
        rand = random.randint(0, 20)
        if rand % 2 == 0:
            cadet.volunteer_hours_status = True
            cadet.save()


def assign_gender_to_males():
    for cadet in cadets:
        if cadet.gender != "Female":
            cadet.gender = "Male"


def assign_at_risk_cadets():
    for cadet in cadets:
        rand = random.randint(0, 20)
        if rand % 8 == 0:
            cadet.at_risk = True
            cadet.save()


def assign_nursing_cadets():
    for cadet in cadets:
        rand = random.randint(0, 20)
        if rand % 8 == 0:
            cadet.nurse_contracted = True
            cadet.save()


def assign_demographics():
    if Demographic.objects.all():
        for cadet in cadets:
            demographics_count = Demographic.objects.all().__len__()
            rand = random.randint(1, demographics_count)
            cadet.demographic = Demographic.objects.get(id=rand)
            cadet.save()

#should not be called in the populate function
def get_gpa(cadets):
        sum_gpa = 0
        cadets_with_gpa = 0
        for cadet in cadets:
            if cadet.gpa > 0:
                cadets_with_gpa += 1
                sum_gpa = sum_gpa + cadet.gpa
        if cadets_with_gpa == 0:
            return 0
        return sum_gpa / cadets_with_gpa

def generate_profiles():
    for cadet in cadets:
        rand = random.randint(0, 20)
        if rand % 3 == 0:
            cadet.on_profile = True
            cadet.profile_reason = "Needs more water."
            cadet.save()

def generate_snapshots(date, start, end):
    current_cadets = Cadet.objects.all()[start:end].__len__()
    males = Cadet.objects.filter(gender='Male')[start:end].__len__()
    females = Cadet.objects.filter(gender='Female')[start:end].__len__()
    contracted_cadets = Cadet.objects.filter(contracted=True)[start:end].__len__()
    smp_cadets = Cadet.objects.filter(smp=True)[start:end].__len__()

    ms1 = MsLevel.objects.get(name="MS1")
    ms2 = MsLevel.objects.get(name="MS2")
    ms3 = MsLevel.objects.get(name="MS3")
    ms4 = MsLevel.objects.get(name="MS4")

    ms1_count = Cadet.objects.filter(ms_level=ms1)[start:end].__len__()
    ms2_count = Cadet.objects.filter(ms_level=ms2)[start:end].__len__()
    ms3_count = Cadet.objects.filter(ms_level=ms3)[start:end].__len__()
    ms4_count = Cadet.objects.filter(ms_level=ms4)[start:end].__len__()

    avg_gpa = get_gpa(Cadet.objects.all()[start:end])
    avg_ms1_gpa = get_gpa(cadets.filter(ms_level=ms1))
    avg_ms2_gpa = get_gpa(cadets.filter(ms_level=ms2))
    avg_ms3_gpa = get_gpa(cadets.filter(ms_level=ms3))
    avg_ms4_gpa = get_gpa(cadets.filter(ms_level=ms4))

    try:
        SnapShot.objects.get(date=date)
        return None
    except:
        pass

    snap = SnapShot.objects.get_or_create(date=date, cadets=current_cadets, males=males, females=females, contracted_cadets=contracted_cadets,
                                          smp_cadets=smp_cadets, ms1_count=ms1_count, ms2_count=ms2_count, ms3_count=ms3_count,
                                          ms4_count=ms4_count, avg_gpa=avg_gpa, avg_ms1_gpa=avg_ms1_gpa, avg_ms2_gpa=avg_ms2_gpa,
                                          avg_ms3_gpa=avg_ms3_gpa, avg_ms4_gpa=avg_ms4_gpa)
    return snap


def create_graders():
    # Male two-mile graders
    grader2 = Grader.objects.get_or_create(gender="Male", activity="Two-mile run", age_group="17-21",
                                           score_table=RUBRIC_MALE_17_21_RUNNING)
    grader3 = Grader.objects.get_or_create(gender="Male", activity="Two-mile run", age_group="22-26",
                                           score_table=RUBRIC_MALE_22_26_RUNNING)
    grader4 = Grader.objects.get_or_create(gender="Male", activity="Two-mile run", age_group="27-31",
                                           score_table=RUBRIC_MALE_27_31_RUNNING)
    grader5 = Grader.objects.get_or_create(gender="Male", activity="Two-mile run", age_group="32-36",
                                           score_table=RUBRIC_MALE_32_36_RUNNING)
    grader6 = Grader.objects.get_or_create(gender="Male", activity="Two-mile run", age_group="37-41",
                                           score_table=RUBRIC_MALE_37_41_RUNNING)

    # Female two-mile graders
    grader7 = Grader.objects.get_or_create(gender="Female", activity="Two-mile run", age_group="17-21",
                                           score_table=RUBRIC_FEMALE_17_21_RUNNING)
    grader8 = Grader.objects.get_or_create(gender="Female", activity="Two-mile run", age_group="22-26",
                                           score_table=RUBRIC_FEMALE_22_26_RUNNING)
    grader9 = Grader.objects.get_or_create(gender="Female", activity="Two-mile run", age_group="27-31",
                                           score_table=RUBRIC_FEMALE_27_31_RUNNING)
    grader10 = Grader.objects.get_or_create(gender="Female", activity="Two-mile run", age_group="32-36",
                                            score_table=RUBRIC_FEMALE_32_36_RUNNING)
    grader11 = Grader.objects.get_or_create(gender="Female", activity="Two-mile run", age_group="37-41",
                                            score_table=RUBRIC_FEMALE_37_41_RUNNING)

    # Male pushups graders
    Grader.objects.get_or_create(gender="Male", activity="Pushups", age_group="17-21",
                                 score_table=RUBRIC_MALE_17_21_PUSHUPS)
    Grader.objects.get_or_create(gender="Male", activity="Pushups", age_group="22-26",
                                 score_table=RUBRIC_MALE_22_26_PUSHUPS)
    Grader.objects.get_or_create(gender="Male", activity="Pushups", age_group="27-31",
                                 score_table=RUBRIC_MALE_27_31_PUSHUPS)
    Grader.objects.get_or_create(gender="Male", activity="Pushups", age_group="32-36",
                                 score_table=RUBRIC_MALE_32_36_PUSHUPS)
    Grader.objects.get_or_create(gender="Male", activity="Pushups", age_group="37-41",
                                 score_table=RUBRIC_MALE_37_41_PUSHUPS)

    # Female pushups graders
    Grader.objects.get_or_create(gender="Female", activity="Pushups", age_group="17-21",
                                 score_table=RUBRIC_FEMALE_17_21_PUSHUPS)
    Grader.objects.get_or_create(gender="Female", activity="Pushups", age_group="22-26",
                                 score_table=RUBRIC_FEMALE_22_26_PUSHUPS)
    Grader.objects.get_or_create(gender="Female", activity="Pushups", age_group="27-31",
                                 score_table=RUBRIC_FEMALE_27_31_PUSHUPS)
    Grader.objects.get_or_create(gender="Female", activity="Pushups", age_group="32-36",
                                 score_table=RUBRIC_FEMALE_32_36_PUSHUPS)
    Grader.objects.get_or_create(gender="Female", activity="Pushups", age_group="37-41",
                                 score_table=RUBRIC_FEMALE_37_41_PUSHUPS)

    # Male situps graders
    Grader.objects.get_or_create(gender="Male", activity="Situps", age_group="17-21",
                                 score_table=RUBRIC_MALE_17_21_SITUPS)
    Grader.objects.get_or_create(gender="Male", activity="Situps", age_group="22-26",
                                 score_table=RUBRIC_MALE_22_26_SITUPS)
    Grader.objects.get_or_create(gender="Male", activity="Situps", age_group="27-31",
                                 score_table=RUBRIC_MALE_27_31_SITUPS)
    Grader.objects.get_or_create(gender="Male", activity="Situps", age_group="32-36",
                                 score_table=RUBRIC_MALE_32_36_SITUPS)
    Grader.objects.get_or_create(gender="Male", activity="Situps", age_group="37-41",
                                 score_table=RUBRIC_MALE_37_41_SITUPS)

    # Female situps graders
    Grader.objects.get_or_create(gender="Female", activity="Situps", age_group="17-21",
                                 score_table=RUBRIC_FEMALE_17_21_SITUPS)
    Grader.objects.get_or_create(gender="Female", activity="Situps", age_group="22-26",
                                 score_table=RUBRIC_FEMALE_22_26_SITUPS)
    Grader.objects.get_or_create(gender="Female", activity="Situps", age_group="27-31",
                                 score_table=RUBRIC_FEMALE_27_31_SITUPS)
    Grader.objects.get_or_create(gender="Female", activity="Situps", age_group="32-36",
                                 score_table=RUBRIC_FEMALE_32_36_SITUPS)
    Grader.objects.get_or_create(gender="Female", activity="Situps", age_group="37-41",
                                 score_table=RUBRIC_FEMALE_37_41_SITUPS)


if __name__ == '__main__':
    print "Starting Eagletrack Population script..."
    from personnel.models import Cadet, Company, Platoon, MsLevel

    populate()
    print "Population script has ran successfully"
