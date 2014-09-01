from django import template
from personnel.models import MsLevel

register = template.Library()


@register.filter(name='interpret_bool')
def interpret_bool(value):
    if value == True:
        return 'Yes'
    elif value == False:
        return 'No'


@register.filter(name='default_blank')
def default_blank(value):
    if value == None:
        return ' '


@register.filter(name='active_cadet')
def active_cadet(dropped, commissioned=False):
    if dropped == False:
        if commissioned == False:
            return "Active"
    if dropped == True:
        return "Dropped"
    if commissioned == True:
        return "Commissioned"
    if dropped == True:
        if commissioned == True:
            return "Error: Dropped and Comissioned = True"


@register.filter(name="active_color")
def active_color(dropped, commissioned=False):
    if dropped is False:
        if commissioned is False:
            return "#00b300"  # green
    if dropped is True:
        return "#FF0000"  # red
    if commissioned is True:
        return "#000000"  # black
    if dropped is True:
        if commissioned is True:
            return "#FF0000"  # red


@register.filter(name='phone_format')
def phone_format(number):
    if len(number) == 10:
        return '(%s)-%s-%s' % (number[:3], number[3:6], number[6:10])


@register.filter(name='class_filter')
def class_filter(cadets, ms_class):
    ms = MsLevel.objects.get(name=ms_class)
    return cadets.filter(ms_level=ms)