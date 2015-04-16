from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from personnel.models import Cadet, Company, Squad, Problems


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

    cell_number = forms.CharField(widget=forms.TextInput(attrs={'Placeholder': 'EX Format: 1234567890 (No dashes)'}))
    car_model = forms.CharField(widget=forms.TextInput(attrs={'Placeholder': 'Enter "None" if this is not applicable'}))
    car_tag = forms.CharField(widget=forms.TextInput(attrs={'Placeholder': 'Enter "None" if this is not applicable'}))
    birth_date = forms.CharField(widget=forms.HiddenInput(attrs={'data-date-format': 'YYYY-mm-dd'}))

    class Meta():
        model = Cadet
        exclude = ['user', 'comments', 'profile_reason', 'events_missed', 'class_events_missed', 'lab_events_missed',
                   'pt_missed', 'attendance_rate', 'ranger_challenge', 'color_guard', 'school', 'dropped', 'commissioned',
                   'volunteer_hours_completed', 'volunteer_hours_count', 'ms_grade', 'company', 'platoon']


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