from personnel.models import Cadet
from pt.models import PtScore, PtTest

#Shared functionality between all stat pages
def grouping_data(cadets):

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
    cumalitive_score_dict = {}
    for cadet in cadets:
        cadet_scores = PtScore.objects.filter(cadet=cadet)
        score = PtScore.get_avg_total_score(cadet_scores) / float(100)
        cumalitive = score + float(cadet.gpa)
        cumalitive_score_dict[cumalitive] = cadet
    return PtTest.order_scores_dict(cumalitive_score_dict, 5)
