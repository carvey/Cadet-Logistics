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

    #Get the top n cadets
    top_scores = PtScore.get_top_cadets(cadets)

    top_gpas = Cadet.get_top_gpa_cadets(cadets, 5)

    ms_levels = {}
    for cadet in cadets:
        if cadet.ms_level in ms_levels:
            ms_levels[cadet.ms_level] += 1
        else:
            ms_levels[cadet.ms_level] = 0
    print ms_levels
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
               'ms_levels': ms_levels
               }
    return context

