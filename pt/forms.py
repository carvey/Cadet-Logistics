from django import forms
from pt.models import PtTest, PtScore


class TestForm(forms.ModelForm):

    class Meta():
        model = PtTest
        exclude = []


class ScoreForm(forms.ModelForm):
    cadet = forms.CharField()

    class Meta():
        model = PtScore
        fields = ['cadet', 'pushups', 'situps', 'two_mile']