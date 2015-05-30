
from django.forms import Widget

class DatePicker(Widget):

    def render(self, name, value, attrs=None):

        return u"<div id='birth_datepicker' 'data-date-format': 'YYYY-mm-dd'></div>"
