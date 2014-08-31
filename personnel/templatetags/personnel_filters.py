from django import template

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
    if dropped == False:
        if commissioned == False:
            return "#00b300"  # green
    if dropped == True:
        return "#FF0000"  # red
    if commissioned == True:
        return "#000000"  # black
    if dropped == True:
        if commissioned == True:
            return "#FF0000"  # red


@register.filter(name='phone_format')
def phone_format(number):
    if len(number) == 10:
        return '(%s)-%s-%s' % (number[:3], number[3:6], number[6:10])