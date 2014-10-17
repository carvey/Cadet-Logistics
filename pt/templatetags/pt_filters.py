from django import template
from personnel.models import MsLevel

register = template.Library()

@register.filter(name='get_score')
def get_score(cadet, scores):
    return scores[cadet.id]