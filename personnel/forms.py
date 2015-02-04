from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from personnel.models import Demographic, GENDER_CHOICES, BLOOD_TYPES


class LoginForm(AuthenticationForm):
     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
     password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

     def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data


class Registration(forms.Form):
    pass

class EditCadet(forms.Form):
    eagle_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Eagle Id'}))
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender = forms.TypedChoiceField(choices=GENDER_CHOICES)
    cell_number = forms.CharField()
    blood_type = forms.TypedChoiceField(choices=tuple([(u'', "-----")] + list(BLOOD_TYPES)))
    car_model = forms.CharField()
    car_tag = forms.CharField()
    demographic = forms.TypedChoiceField(choices=Demographic.to_list())

