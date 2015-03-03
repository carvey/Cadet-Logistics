from django import forms
from pt.models import PtTest, PtScore
from personnel.models import Cadet


class TestForm(forms.ModelForm):

    class Meta():
        model = PtTest
        exclude = []


class ScoreForm(forms.Form):
    cadet = forms.CharField()
    cadet_id = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'cadet_id'}))
    pushups = forms.IntegerField(initial=None, widget=forms.NumberInput(attrs={'placeholder': 0}))
    situps = forms.IntegerField(initial=None, widget=forms.NumberInput(attrs={'placeholder': 0}))
    two_mile = forms.CharField(initial=None, widget=forms.TextInput(attrs={'placeholder': '00:00'}))
