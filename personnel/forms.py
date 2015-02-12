from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from personnel.models import Demographic, GENDER_CHOICES, BLOOD_TYPES, Cadet


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


class EditCadet(forms.ModelForm):

    class Meta():
        model = Cadet
        fields = ['eagle_id', 'cell_number', 'blood_type', 'car_model', 'car_tag']


class EditCadetFull(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(EditCadetFull, self).__init__(*args, **kwargs)
    #
    #     for field in self.fields:
    #         self.fields[field].required = False

    class Meta():
        model = Cadet
        exclude = ['objects', 'user', 'events_missed', 'class_events_missed',
                   'lab_events_missed', 'pt_missed', 'attendance_rate', 'school']


class EditCadetUser(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(EditCadetUser, self).__init__(*args, **kwargs)
    #
    #     for field in self.fields:
    #         self.fields[field].required = False

    class Meta():
        model = User
        exclude = ['date_joined', 'last_login', 'superuser_status', 'password', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'is_superuser']