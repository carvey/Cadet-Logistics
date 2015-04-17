from personnel.models import Cadet, Company, Platoon, Squad
from pt.models import PtScore, PtTest
from personnel.forms import CompanyStaffForm

#Shared functionality between all stat pages
def grouping_data(cadets):
    """
    This generates a ton of grouping related data over a subset of cadets
    :param cadets: The subset of cadets to calculate over
    :return: context dict
    """
    contracted = cadets.filter(contracted=True)
    smp = cadets.filter(smp=True)
    avg_gpa = Cadet.get_avg_gpa(cadets)
    at_risk = cadets.filter(at_risk=True)
    profiles = cadets.filter(on_profile=True)
    male_cadets = cadets.filter(gender='Male')
    female_cadets = cadets.filter(gender='Female')
    completed_volunteer_hours = cadets.filter(volunteer_hours_completed=True)

    #Get the top n cadets
    top_scores = PtScore.get_top_cadets(cadets)

    top_gpas = Cadet.get_top_gpa_cadets(cadets, 5)

    top_cumalitive_scores = top_cumulative_scores(cadets)

    ms_levels = {}
    for cadet in cadets:
        if cadet.ms_level in ms_levels:
            ms_levels[cadet.ms_level] += 1
        else:
            ms_levels[cadet.ms_level] = 0

    scores_by_test = {}
    tests = PtTest.filtered_tests.all()
    for test in tests:
        scores = PtScore.objects.filter(pt_test=test, cadet__in=cadets)
        if scores:
            test_dict = {}
            test_dict.update({'pushups': PtScore.get_avg_pushup_score(scores),
                              'situps': PtScore.get_avg_situp_score(scores),
                              'run': PtScore.get_avg_run_score(scores),
                              'total': PtScore.get_avg_total_score(scores)})
            scores_by_test.update({test: test_dict})

    context = {
        'cadets': cadets,
        'contracted_cadets': contracted,
        'smp_cadets': smp,
        'avg_gpa': avg_gpa,
        'at_risk_cadets': at_risk,
        'profiles': profiles,
        'male_cadets': male_cadets,
        'female_cadets': female_cadets,
        'completed_hours': completed_volunteer_hours,
        'top_scores': top_scores,
        'top_gpas': top_gpas,
        'top_cumulative_scores': top_cumalitive_scores,
        'ms_levels': ms_levels,
        'scores_by_test': scores_by_test,
        }
    return context


def top_cumulative_scores(cadets):
    """
    Takes a subset of cadets and generates a sort of ranking for the cadet using a combination of GPA
    and avg PT score

    cumulative_score = GPA + (avg_pt_score/100)

    So a GPA of 4.0 and an avg pt score of 297 would look like
    cumulative_score = 4.0 + 2.97
                     = 6.97

    :param cadets: The subset of cadets to calculate scores over
    :return:
    """
    cumalitive_score_dict = {}
    for cadet in cadets:
        if cadet.gpa:
            cadet_scores = PtScore.objects.filter(cadet=cadet)
            score = PtScore.get_avg_total_score(cadet_scores) / float(100)
            cumalitive = score + float(cadet.gpa)
        if cumalitive in cumalitive_score_dict:
            #if this value is already a list (more than 2 cadets with score score already), then append the cadet
            if isinstance(cumalitive_score_dict[cumalitive], list):
                cumalitive_score_dict[cumalitive].append(cadet)
                #if this is the first occurrence of repeated scores, then make a list out of the two cadets
            else:
                cumalitive_score_dict[cumalitive] = [cumalitive_score_dict[cumalitive], cadet]
                #no repeated scores, so just insert the score and cadet as a default key,value pair
        else:
            cumalitive_score_dict.update({cumalitive: cadet})
    return PtTest.order_scores_dict(cumalitive_score_dict, 5)

# TODO docstring needs updating
def assemble_staff_hierarchy():
    """
    Should assemble a dict of the form
    { company: { platoon: [squads] } }

    EX:
        { alpha company: {platoon1: [squad1, squad2], platoon2: [squad1, squad2] },
          bravo company: {platoon1: [squad1, squad2], platoon2: [squad1, squad2] }

    :return: dict containing the entire structure of the battalion
    """
    batallion_dict = {}
    for company in Company.objects.all():
        platoon_dict = {}
        for platoon in company.platoons.all():
            platoon_dict[platoon] = [squad for squad in platoon.squads.all()]
        form = CompanyStaffForm(initial={
            'company': company,
            'commander': company.company_commander,
            'first_sgt': company.first_sergeant,
            'xo': company.executive_officer
        })
        batallion_dict[company] = (form, platoon_dict)
    return batallion_dict