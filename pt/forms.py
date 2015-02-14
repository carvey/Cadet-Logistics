from django import forms
from pt.models import PtTest


class AddTestForm(forms.ModelForm):

    class Meta():
        model = PtTest
        exclude = []