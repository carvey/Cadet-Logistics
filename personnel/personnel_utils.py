from personnel.models import Cadet
from pt.models import PtScore
from django.core.exceptions import ObjectDoesNotExist
import collections


#Shared functionality between all stat pages
def grouping_data(cadets):

    contracted = cadets.filter(contracted=True)
    smp = cadets.filter(smp=True)
    avg_gpa = Cadet.get_avg_gpa(cadets)
    at_risk = cadets.filter(at_risk=True)
    profiles = cadets.filter(on_profile=True)
    male_cadets = cadets.filter(gender='Male')
    female_cadets = cadets.filter(gender='Female')
    completed_volunteer_hours = cadets.filter(volunteer_hours_status=True)

    #Get the top 3 cadets
    all_scores = PtScore.objects.all()
    avg_scores = {}
    ptscore = PtScore()
    for cadet in cadets:
        scores = all_scores.filter(cadet=cadet)
        avg_scores[cadet] = PtScore.get_avg_total_score(scores)
    avg_scores = collections.OrderedDict(reversed(sorted(avg_scores.items(), key=lambda t: t[1])))
    top_scores = collections.OrderedDict()
    count = 0
    for x, y in avg_scores.items():
        top_scores.update({y: x})
        count += 1
        if count == 5: #the number of top cadets to get
            break

    top_gpas = Cadet.get_top_gpa_cadets(cadets, 5)

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
               'top_scores': reversed(sorted(top_scores.items())),
               'top_gpas': top_gpas
               }
    return context

