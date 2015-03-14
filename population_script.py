import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eagletrack_project.settings')


from personnel.models import *
from pt.models import *
from pt.constants import *
import sys, datetime, random
from django.contrib.auth.models import User

sys.path.append(os.path.dirname(__file__))

# Create your tests here.
cadets = Cadet.objects.all()

def clear_cadets():
    for cadet in Cadet.objects.all():
        cadet.delete()


def populate():
    print "clearing cadets"
    #use this for when snapshots need testing, otherwise comment it out
    clear_cadets()
    print "done clearing cadets"
    print "-----------------------"

    print "Creating companies"
    alpha = add_company(name="Alpha")
    bravo = add_company(name="Bravo")
    charlie = add_company(name="Charlie")
    delta = add_company(name="Delta")
    print "done creating companies"
    print "-----------------------"

    print "creating platoons and squads"

    """
    Naming Scheme:
        Platoons: company name + platoon number
        Squads:  company name + platoon number + squad number
    """
    alpha1st = add_platoon(name=1, company=alpha)
    alpha11 = add_squad(name=1, platoon=alpha1st)
    alpha12 = add_squad(name=2, platoon=alpha1st)

    bravo1st = add_platoon(name=1, company=bravo)
    bravo11 = add_squad(name=1, platoon=bravo1st)
    bravo12 = add_squad(name=2, platoon=bravo1st)
    bravo2nd = add_platoon(name=2, company=bravo)
    bravo21 = add_squad(name=1, platoon=bravo2nd)
    bravo22 = add_squad(name=2, platoon=bravo2nd)

    charlie1st = add_platoon(name=1, company=charlie)
    charlie11 = add_squad(name=1, platoon=charlie1st)
    charlie12 = add_squad(name=2, platoon=charlie1st)
    charlie2nd = add_platoon(name=2, company=charlie)
    charlie21 = add_squad(name=1, platoon=charlie2nd)
    charlie22 = add_squad(name=2, platoon=charlie2nd)

    delta1st = add_platoon(name=1, company=delta)
    delta11 = add_squad(name=1, platoon=delta1st)
    delta12 = add_squad(name=2, platoon=delta1st)
    delta2nd = add_platoon(name=2, company=delta)
    delta21 = add_squad(name=1, platoon=delta2nd)
    delta22 = add_squad(name=2, platoon=delta2nd)
    print "done creating platoons"
    print "-----------------------"

    print "adding ms levels"
    # adding ms levels
    ms1 = add_mslevel(name="MS1")
    ms2 = add_mslevel(name="MS2")
    ms3 = add_mslevel(name="MS3")
    ms4 = add_mslevel(name="MS4")
    print "done adding ms levels"
    print "-----------------------"

    print "Adding demographics"
    add_demographic(demographic="White")
    add_demographic(demographic="Black")
    add_demographic(demographic="Asian")
    add_demographic(demographic="American Indian")
    add_demographic(demographic="Hispanic")
    print "done adding demographics"
    print "-----------------------"


    print "Creating cadets"
    #Alpha Company
    add_cadet(first_name="Adam", last_name="Kostner", age=20, ms_level=ms4, company=alpha, cc=True)
    add_cadet(first_name="Cole", last_name="Stuart", age=20, ms_level=ms4, company=alpha, fs=True)
    add_cadet(first_name="Taylor", last_name="Cooper", age=20, ms_level=ms4, company=alpha, platoon=alpha1st, squad=alpha11, sl=True)
    add_cadet(first_name="Jason", last_name="Canter", age=20, ms_level=ms4, company=alpha, platoon=alpha1st, squad=alpha11)
    add_cadet(first_name="Eddie", last_name="Hanson", age=20, ms_level=ms4, company=alpha, platoon=alpha1st, squad=alpha12, sl=True)
    add_cadet(first_name="Ashley", last_name="Scott", age=20, gender="Female", ms_level=ms4, company=alpha, platoon=alpha1st, squad=alpha12)
    add_cadet(first_name="Danial", last_name="Miller", age=20, ms_level=ms3, company=alpha, platoon=alpha1st, squad=alpha12)


    #Bravo company
    add_cadet(first_name="James", last_name="Lee", age=20, ms_level=ms3, company=bravo, cc=True)
    add_cadet(first_name="Joanna", last_name="Henry", age=20, ms_level=ms3, company=bravo, fs=True)
    #Bravo 1st platoon
    add_cadet(first_name="Kyle", last_name="Jackson", age=20, ms_level=ms3, company=bravo, platoon=bravo1st, pc=True)
    add_cadet(first_name="Kathy", last_name="Jones", age=20, gender="Female", ms_level=ms3, company=bravo, platoon=bravo1st, ps=True)
    add_cadet(first_name="Kellie", last_name="Rogers", age=19, gender="Female", ms_level=ms2, company=bravo, platoon=bravo1st, squad=bravo11, sl=True)
    add_cadet(first_name="Oliver", last_name="Paige", age=20, gender="Female", ms_level=ms2, company=bravo, platoon=bravo1st, squad=bravo11)
    add_cadet(first_name="Trenton", last_name="Francis", age=19, ms_level=ms2, company=bravo, platoon=bravo1st, squad=bravo11)
    add_cadet(first_name="Samantha", last_name="Roberts", age=19, gender="Female", ms_level=ms2, company=bravo, platoon=bravo1st, squad=bravo12, sl=True)
    add_cadet(first_name="Robert", last_name="Bacon", age=19, ms_level=ms2, company=bravo, platoon=bravo1st, squad=bravo12)
    add_cadet(first_name="Samual", last_name="Gates", age=19, ms_level=ms2, company=bravo, platoon=bravo1st, squad=bravo12)
    #Bravo 2nd Platoon
    add_cadet(first_name="George", last_name="Hart", age=20, ms_level=ms3, company=bravo, platoon=bravo2nd, pc=True)
    add_cadet(first_name="Wilson", last_name="Cooper", age=20, ms_level=ms3, company=bravo, platoon=bravo2nd, ps=True)
    add_cadet(first_name="Thomas", last_name="Lee", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd, squad=bravo21, sl=True)
    add_cadet(first_name="Jennifer", last_name="Stone", age=19, gender="Female", ms_level=ms2, company=bravo, platoon=bravo2nd, squad=bravo21)
    add_cadet(first_name="Eva", last_name="Lowry", age=20, gender="Female", ms_level=ms2, company=bravo, platoon=bravo2nd, squad=bravo21)
    add_cadet(first_name="Michael", last_name="Han", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd, squad=bravo21)
    add_cadet(first_name="Kathy", last_name="Marino", age=19, gender="Female", ms_level=ms2, company=bravo, platoon=bravo2nd, squad=bravo22, sl=True)
    add_cadet(first_name="James", last_name="Cooper", age=19, ms_level=ms2, company=bravo, platoon=bravo2nd, squad=bravo22)


    #Charlie Company
    add_cadet(first_name="Sarah", last_name="Klein", age=20, gender="Female", ms_level=ms3, company=charlie, cc=True)
    add_cadet(first_name="Kenny", last_name="Walts", age=20, ms_level=ms3, company=charlie, fs=True)
    #Charlie First Platoon
    add_cadet(first_name="Matthew", last_name="Henry", age=20, ms_level=ms3, company=charlie, platoon=charlie1st, pc=True)
    add_cadet(first_name="Audrey", last_name="Chantel", age=20, gender="Female", ms_level=ms3, company=charlie, platoon=charlie1st, ps=True)
    add_cadet(first_name="Mary", last_name="Jones", age=18, gender="Female", ms_level=ms1, company=charlie, platoon=charlie1st, squad=charlie11, sl=True)
    add_cadet(first_name="Roger", last_name="Alan", age=18, ms_level=ms1, company=charlie, platoon=charlie1st, squad=charlie11)
    add_cadet(first_name="Joshua", last_name="Springer", age=20, ms_level=ms2, company=charlie, platoon=charlie1st, squad=charlie12, sl=True)
    add_cadet(first_name="Pablo", last_name="Smith", age=18, ms_level=ms1, company=charlie, platoon=charlie1st, squad=charlie12)
    #Charlie 2nd Platoon
    add_cadet(first_name="Gordon", last_name="Miles", age=20, ms_level=ms3, company=charlie, platoon=charlie2nd, pc=True)
    add_cadet(first_name="Mia", last_name="Scott", age=20, gender="Female", ms_level=ms3, company=charlie, platoon=charlie2nd, ps=True)
    add_cadet(first_name="Brett", last_name="Cade", age=20, ms_level=ms2, company=charlie, platoon=charlie2nd, squad=charlie21, sl=True)
    add_cadet(first_name="Garret", last_name="Timpson", age=18, ms_level=ms1, company=charlie, platoon=charlie2nd, squad=charlie21)
    add_cadet(first_name="Julia", last_name="Anderson", age=18, gender="Female", ms_level=ms1, company=charlie, platoon=charlie2nd, squad=charlie22, sl=True)
    add_cadet(first_name="Chris", last_name="Danials", age=20, ms_level=ms2, company=charlie, platoon=charlie2nd, squad=charlie22)


    #Delta company
    add_cadet(first_name="Nick", last_name="Russel", age=20, ms_level=ms3, company=delta, cc=True)
    add_cadet(first_name="Melissa", last_name="Hackman", age=20, gender="Female", ms_level=ms3, company=delta, fs=True)
    #First Platoon
    add_cadet(first_name="Alexander", last_name="May", age=20, ms_level=ms3, company=delta, platoon=delta1st, pc=True)
    add_cadet(first_name="Jeff", last_name="Sleet", age=20, ms_level=ms3, company=delta, platoon=delta1st, ps=True)
    add_cadet(first_name="Joe", last_name="Taylor", age=18, ms_level=ms1, company=delta, platoon=delta1st, squad=delta11, sl=True)
    add_cadet(first_name="Jim", last_name="Bob", age=18, ms_level=ms1, company=delta, platoon=delta1st, squad=delta11)
    add_cadet(first_name="Gordon", last_name="Thomas", age=20, ms_level=ms2, company=delta, platoon=delta1st, squad=delta12, sl=True)
    add_cadet(first_name="Isabella", last_name="Miller", age=19, gender="Female", ms_level=ms2, company=delta, platoon=delta1st, squad=delta12)
    #Second Platoon
    add_cadet(first_name="Steve", last_name="Bolhman", age=20, ms_level=ms3, company=delta, platoon=delta2nd, pc=True)
    add_cadet(first_name="Eric", last_name="Greenwood", age=20, ms_level=ms3, company=delta, platoon=delta2nd, ps=True)
    add_cadet(first_name="Alan", last_name="Smith", age=18, ms_level=ms1, company=delta, platoon=delta2nd, squad=delta21, sl=True)
    add_cadet(first_name="Cody", last_name="Gruff", age=19, ms_level=ms2, company=delta, platoon=delta2nd, squad=delta21)
    add_cadet(first_name="Jane", last_name="West", age=18, gender="Female", ms_level=ms1, company=delta, platoon=delta2nd, squad=delta22, sl=True)
    add_cadet(first_name="Anne", last_name="Locke", age=18, gender="Female", ms_level=ms1, company=delta, platoon=delta2nd, squad=delta22)
    print "Done creating cadets"
    print "-----------------------"

    print "Creating Cadre"
    add_cadre(first_name="Roger", last_name="Smith", age=30, rank="Captain", position="XO")
    print "Done create cadre"
    print "-----------------------"



    print "Creating pt tests"
    add_pt_test(date=datetime.date(2014, 6, 1) + datetime.timedelta(days=2), ms_classes=[ms4])
    add_pt_test(date=datetime.date(2014, 6, 1) + datetime.timedelta(days=5), ms_classes=[ms1, ms2, ms3])
    add_pt_test(date=datetime.date(2014, 6, 1) + datetime.timedelta(days=7), ms_classes=[ms1, ms2, ms3])
    print "Done adding pt tests"
    print "-----------------------"

    print "creating pt scores"
    create_pt_scores()
    print "done creating pt scores"
    print "-----------------------"

    print "assigning eagle ids"
    assign_eagle_id()
    print "done assigning eagle id's"
    print "-----------------------"

    print "assigning cell nums"
    assign_cell_num()
    print "Done assigning cell nums"
    print "-----------------------"

    print "assinging emails"
    assign_email()
    print "Done assigning emails"
    print "-----------------------"

    print "assigning gpas"
    assign_gpa()
    print "Done assigning gpa's"
    print "-----------------------"

    print "assigning ms grade"
    assign_ms_grade()
    print "Done assigning ms grades"
    print "-----------------------"

    print "assinging contracts and smps to cadets"
    assign_contract_smp()
    print "done assigning contracted and smp to cadets"
    print "-----------------------"

    print "assigning gender to males"
    assign_gender_to_males()
    print "Done assinging gender to males"
    print "-----------------------"

    print "generating volunteer completion"
    generate_volunteer_completion()
    print "Done generating volunteer completion"
    print "-----------------------"

    print "assigning nursing cadets"
    assign_nursing_cadets()
    print "Done assigning nursing cadets"
    print "-----------------------"

    print "assigning demographics"
    assign_demographics()
    print "Done assigning demographics"
    print "-----------------------"

    print "assigning at risk cadets"
    assign_at_risk_cadets()
    print "Done assigning at risk cadets"
    print "-----------------------"

    print "generating profiles"
    generate_profiles()
    print "Done generating profiles"
    print "-----------------------"

    print "Generating Snapshots"
    generate_snapshots(date = datetime.date(2014, 6, 1), start=0, end=0)
    generate_snapshots(date = datetime.date(2014, 7, 1), start=0, end=3)
    generate_snapshots(date = datetime.date(2014, 8, 1), start=0, end=12)
    generate_snapshots(date = datetime.date(2014, 9, 1), start=0, end=15)
    generate_snapshots(date = datetime.date(2014, 10, 1), start=0, end=23)
    generate_snapshots(date = datetime.date(2014, 11, 1), start=0, end=21)
    generate_snapshots(date = datetime.date(2014, 12, 1), start=0, end=30)
    print "Done generating Snapshots"
    print "-----------------------"

    print "Creating graders"
    create_graders()
    print "Done creating Graders"
    print "-----------------------"
    #generate_pt_score_value()


def add_company(name, co=None, fs=None):
    company = Company.objects.get_or_create(name=name, company_commander=co, first_sergeant=fs)[0]
    return company


def add_platoon(name, company):
    platoon = Platoon.objects.get_or_create(name=name, company=company)[0]
    return platoon


def add_squad(name, platoon):
    squad = Squad.objects.get_or_create(name=name, platoon=platoon)[0]
    return squad

def add_cadet(first_name, last_name, age, ms_level, company, squad=None, gender="Male", platoon=None, ms_grade=100,
               cc=False, fs=False, pc=False, ps=False, sl=False):

    user = User.objects.get_or_create(username=(first_name+last_name).lower(), first_name=first_name, last_name=last_name)[0]
    user.set_password('pass')
    user.save()

    c = Cadet.objects.get_or_create(user=user, age=age, gender=gender, ms_level=ms_level,
                                    company=company, platoon=platoon, squad=squad)[0]

    if cc:
        company.set_commander(c)
    elif fs:
        company.set_first_sergeant(c)
    elif pc:
        platoon.set_platoon_commander(c)
    elif ps:
        platoon.set_platoon_sergeant(c)
    elif sl:
        squad.set_squad_leader(c)

    return c


def add_cadre(first_name, last_name, age, rank, position):

    user = User.objects.get_or_create(username=(first_name+last_name).lower(), first_name=first_name, last_name=last_name)[0]
    user.set_password('pass')
    user.save()

    c = Cadre.objects.get_or_create(user=user, age=age, rank=rank, position=position)

    return c

def add_mslevel(name):
    ms = MsLevel.objects.get_or_create(name=name)[0]
    return ms


def add_pt_test(date, ms_classes):
    pt_test = PtTest.objects.get_or_create(date=date)[0]
    for ms_level in ms_classes:
        pt_test.ms_levels.add(ms_level)
    return pt_test


def add_demographic(demographic):
    demo = Demographic.objects.get_or_create(demographic=demographic)
    return demo


def create_pt_scores():
    grader_list = Cadet.objects.filter(ms_level__name='MS4' and 'MS3')
    pt_tests = PtTest.objects.all()
    for test in pt_tests:
        ms_classes = [ms for ms in test.ms_levels.all()]
        for cadet in Cadet.objects.filter(ms_level__in=ms_classes):
            cadet_score = None
            try:
                cadet_score = PtScore.objects.get(cadet=cadet, pt_test=test) #checks to see whether a ptscore has already been created for this test and cadet
                cadet_score.save()
            except:
                pass
            if cadet_score is None:
                score = PtScore.objects.get_or_create(grader=random.choice(grader_list), pt_test=test, cadet=cadet, pushups=random.randint(0,80), situps=random.randint(0,80), score=0, two_mile="%s:%s" % (random.randint(12,20), random.randint(0,59)))
                score[0].save()


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
        cadet.user.email = cadet.user.first_name[:1].lower() + cadet.user.last_name.lower() + str(starting_num) + '@georgiasouthern.edu'
        starting_num += 75
        cadet.user.save()


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

    import django
    django.setup()

    populate()
    print "Population script has ran successfully"
