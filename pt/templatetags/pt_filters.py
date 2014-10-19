from django import template

register = template.Library()

@register.filter(name='get_score')
def get_score(cadet, scores):
    return scores[cadet.id]