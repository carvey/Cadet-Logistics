from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from personnel.models import Demographic, GENDER_CHOICES, BLOOD_TYPES, Cadet, Company


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


class UserRegistrationForm(forms.ModelForm):

    school_email = forms.EmailField()
    eagletrack_password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        passwd = self.cleaned_data.get('eagletrack_password')
        confirmed_passwd = self.cleaned_data.get('password_confirmation')

        if passwd != confirmed_passwd:
            raise forms.ValidationError('Password do not match')

        try:
            username = self.cleaned_data['school_email'].rpartition('@')[0]
            user = User.objects.get(username=username)
            print self.__dict__
            raise forms.ValidationError('That Email has already been used for registration')
        except ObjectDoesNotExist:
            pass

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta():
        model = User
        fields = ['first_name', 'last_name']


class CadetRegistrationForm(forms.ModelForm):

    class Meta():
        model = Cadet
        exclude = ['user', 'comments', 'profile_reason', 'events_missed', 'class_events_missed', 'lab_events_missed',
                   'pt_missed', 'attendance_rate', 'ranger_challenge', 'color_guard', 'school', 'dropped', 'commissioned',
                   'volunteer_hours_completed', 'volunteer_hours_count', 'ms_grade']


class EditCadet(forms.ModelForm):


    class Meta():
        model = Cadet
        fields = ['eagle_id', 'cell_number', 'blood_type', 'car_model', 'car_tag']


class EditCadetFull(forms.ModelForm):

    class Meta():
        model = Cadet
        exclude = ['objects', 'user', 'events_missed', 'class_events_missed',
                   'lab_events_missed', 'pt_missed', 'attendance_rate', 'school']


class EditCadetUser(forms.ModelForm):

    class Meta():
        model = User
        exclude = ['date_joined', 'last_login', 'superuser_status', 'password', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'is_superuser']


class AddCompanyForm(forms.ModelForm):

    class Meta():
        model = Company
        exclude = []

class EditCompanyForm(forms.ModelForm):

    class Meta():
        model = Company
        exclude = []