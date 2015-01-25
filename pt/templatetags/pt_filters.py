from django import template
import calendar

register = template.Library()

@register.filter(name='get_score')
def get_score(cadet, scores):
    return scores[cadet.id]

@register.filter(name='timestamp')
def timestamp(snap):
    return calendar.timegm(snap.timetuple()) * 1000

@register.filter(name='is_list')
def is_list(var):
    if isinstance(var, list):
        return True
    else:
        return False