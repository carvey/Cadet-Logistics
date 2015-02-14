from django import template
import calendar

register = template.Library()


@register.filter(name='interpret_bool')
def interpret_bool(value):
    if value:
        return 'Yes'
    else:
        return 'No'

@register.filter(name='interpret_none')
def interpret_none(value):
    if not value:
        return 'None'
    else:
        return value


@register.filter(name='default_blank')
def default_blank(value):
    if value is None:
        return ' '


@register.filter(name='active_cadet')
def active_cadet(dropped, commissioned=False):
    if not dropped:
        if not commissioned:
            return "Active"
    if dropped:
        return "Dropped"
    if commissioned:
        return "Commissioned"
    if dropped:
        if commissioned:
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


@register.filter(name='timestamp')
def timestamp(snap):
    return calendar.timegm(snap.timetuple()) * 1000


@register.filter(name='lookup')
def display_ordereddict(_list, index):
    if index % 2 == 0:
        return _list[0]
    else:
        return _list[1]


@register.filter(name='is_list')
def is_list(var):
    if isinstance(var, list):
        return True
    else:
        return False