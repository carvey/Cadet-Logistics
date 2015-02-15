from django import forms
from pt.models import PtTest


class TestForm(forms.ModelForm):

    class Meta():
        model = PtTest
        exclude = []