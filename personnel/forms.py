import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from personnel.models import Cadet, Company, Squad, Problems, Cadre
from widgets.date_picker import DatePicker


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

    school_email = forms.EmailField(required=True)
    eagletrack_password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        passwd = self.cleaned_data.get('eagletrack_password')
        confirmed_passwd = self.cleaned_data.get('password_confirmation')
        email = self.cleaned_data.get('school_email')

        if passwd and confirmed_passwd:
            if passwd != confirmed_passwd:
                raise forms.ValidationError('Passwords do not match')

        if email:
            try:
                username = email.rpartition('@')[0]
                user = User.objects.get(username=username)
                raise forms.ValidationError('That Email has already been used for registration')
            except ObjectDoesNotExist:
                pass

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.title()

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta():
        model = User
        fields = ['first_name', 'last_name']


class CadreRegistrationForm(forms.ModelForm):

    birth_date = forms.CharField(widget=DatePicker())

    class Meta():
        model = Cadre
        exclude = ['user']


class CadetRegistrationForm(forms.ModelForm):

    birth_date = forms.CharField(widget=forms.HiddenInput(attrs={'data-date-format': 'YYYY-mm-dd'}))

    class Meta():
        model = Cadet
        exclude = ['user', 'comments', 'profile_reason', 'events_missed', 'class_events_missed', 'lab_events_missed',
                   'pt_missed', 'attendance_rate', 'ranger_challenge', 'color_guard', 'school', 'dropped', 'commissioned',
                   'volunteer_hours_completed', 'volunteer_hours_count', 'ms_grade', 'company', 'platoon', 'at_risk']

    def clean_cell_number(self):
        number = self.cleaned_data.get('cell_number')
        return "".join(char for char in number if char.isdigit())

    def clean_birth_date(self):
        raw_date = self.cleaned_data.get('birth_date')
        date = datetime.datetime.strptime(raw_date, "%Y-%m-%d").date()
        today = datetime.date.today()
        if date >= today:
            raise forms.ValidationError("Your birth date must be before today")
        return raw_date


class EditCadet(forms.ModelForm):

    class Meta():
        model = Cadet
        fields = ['eagle_id', 'cell_number', 'blood_type', 'car_model', 'car_tag', 'ms_level']


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


class CompanyStaffForm(forms.Form):

    company = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Company.objects.all())
    commander = forms.ModelChoiceField(queryset=Cadet.objects.all(), required=False)
    commander_new_squad = forms.ModelChoiceField(queryset=Squad.objects.all(), label="Out-going Commander's new squad",
                                                 required=False)
    first_sgt = forms.ModelChoiceField(queryset=Cadet.objects.all(), required=False)
    first_sgt_new_squad = forms.ModelChoiceField(queryset=Squad.objects.all(), label="Outgoing First Sgt's new Squad",
                                                 required=False)
    xo = forms.ModelChoiceField(queryset=Cadet.objects.all(), label="XO", required=False)
    xo_new_squad = forms.ModelChoiceField(queryset=Squad.objects.all(), label="Out-going XO's new squad",
                                          required=False)

    def clean(self):
        company = self.cleaned_data['company']
        commander = self.cleaned_data['commander']
        commander_new_squad = self.cleaned_data.get('commander_new_squad')
        first_sgt = self.cleaned_data['first_sgt']
        first_sgt_new_squad = self.cleaned_data.get('first_sgt_new_squad')
        xo = self.cleaned_data['xo']
        xo_new_squad = self.cleaned_data.get('xo_new_squad')

        if commander and not commander_new_squad:
            if company.company_commander != commander:
                raise forms.ValidationError("If a new Commander is selected, then that commander must be assigned to a new Squad")
            else:
                raise forms.ValidationError("You must select a new squad for the outgoing commander to be placed in")


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problems
        exclude = []