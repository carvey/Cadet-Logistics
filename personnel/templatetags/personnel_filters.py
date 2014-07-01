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
        