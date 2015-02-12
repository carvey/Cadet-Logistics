from django import template

register = template.Library()

@register.filter(name='is_owner')
def is_owner(user, user_from_request):
    """
    Determines whether the user that is logged in is the same as a cadet/cadre instance variable
    :param user: the user that is logged in
    :param user_from_request: the cadet/cadre that is being dealt with in the template (ex: 'cadet' variable from view)
    :return: True, if the logged in user is the same as the user passed in the second arg. False otherwise.
    """
    if user == user_from_request.user:
        return True
    return False

@register.filter(name='has_permission')
def has_permission(user, user_from_request):
    if user == user_from_request.user or hasattr(user, 'cadre') or user.is_superuser:
        return True
    return False