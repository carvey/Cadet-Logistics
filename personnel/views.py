from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from personnel.models import Cadet, Company, MsLevel, Platoon, SnapShot, Demographic, Squad
from pt.models import PtScore, PtTest, Grader
from personnel_utils import grouping_data, assemble_staff_hierarchy
from django.contrib.auth.decorators import login_required
from personnel.forms import LoginForm, EditCadet, EditCadetFull, EditCadetUser, AddCompanyForm, EditCompanyForm,\
    CadetRegistrationForm, UserRegistrationForm, CompanyStaffForm
from django.contrib.auth.views import logout_then_login


class Login(FormView):
    template_name = 'personnel/auth/login.html'
    form_class = LoginForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, next=self.request.GET.get('next')))

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if not user:
            return HttpResponseRedirect('/login')
        login(self.request, user)
        if self.request.POST.get('next') != 'None':
            return HttpResponseRedirect(self.request.POST.get('next'))
        else:
            return super(Login, self).form_valid(form)


def logout(request):
    return logout_then_login(request, login_url='/personnel/login')


class Index(View):
    template_name = "index/index.html"

    def get(self, request):
        tests = PtTest.objects.all()
        context = {
            'tests': tests
        }

        if hasattr(request.user, 'cadet'):
            cadet = request.user.cadet

            context.update({
                'cadet': cadet
            })
        elif hasattr(request.user, 'cadre'):
            cadre = request.user.cadre

            context.update({
                'cadre': cadre
            })

        return render(request, self.template_name, context)


class Stats(View):
    template_name = 'personnel/stat_page/personnel_stats.html'

    def get(self, request, tab='cadets'):
        cadets = Cadet.objects.all()
        current_cadets = cadets.filter(commissioned=False, dropped=False)
        nursing_contracted = cadets.filter(nurse_contracted=True)

        snapshots = SnapShot.objects.all()

        demo_dict = {}
        for cadet in current_cadets:
            if cadet.demographic:
                if cadet.demographic not in demo_dict:
                    demo_dict.update({cadet.demographic: 1})
                else:
                    demo_dict[cadet.demographic] += 1

        context = {
            'tab': tab,
            'snapshots': snapshots,
            'cadets': current_cadets,
            'nursing_contracted': nursing_contracted,
            'demographics': demo_dict,
        }
        context.update(grouping_data(current_cadets))
        return render(request, self.template_name, context)


class CadetListing(View):
    template_name = 'personnel/cadet_listing.html'

    cadets = Cadet.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'cadets': self.cadets})


class CadetRegistration(View):
    template_name = 'personnel/auth/registration/cadet_registration.html'

    def get(self, request):
        user_form = UserRegistrationForm()
        cadet_form = CadetRegistrationForm()
        context = {
            'user_form': user_form,
            'cadet_form': cadet_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        cadet_form = CadetRegistrationForm(request.POST)
        if cadet_form.is_valid() and user_form.is_valid():
            password = user_form.cleaned_data['eagletrack_password']
            email = user_form.cleaned_data['school_email']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']

            cadet = cadet_form.save(commit=False)
            squad = cadet_form.cleaned_data.get('squad')

            username = cadet.generate_username(email)
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            cadet.user = user
            cadet.set_squad(squad)
            cadet.save()
            return HttpResponseRedirect('/')
        else:
            context = {
                'user_form': user_form,
                'cadet_form': cadet_form,
            }
            return render(request, self.template_name, context)


def cadet_page(request, cadet_id, tab='overview'):
    template_name = 'personnel/cadet_page/cadet_page.html'
    form = None
    user_form = None
    cadet = Cadet.objects.get(id=cadet_id)
    context = {}

    scores = PtScore.objects.filter(cadet=cadet_id).order_by('-pt_test')
    ordered_scores = scores.order_by('-pt_test')[:3]

    # initializing pt related vars to 0 ahead of time, in case the cadet has no pt tests yet
    max_score = min_score = avg_score = avg_pushups = avg_situps = avg_two_mile = 0
    avg_pushup_score = avg_situp_score = avg_two_mile_score = 0

    context.update({
        'tab': tab,
        'cadet': cadet,
        'form': form,
        'user_form': user_form
    })

    if scores:
        max_score = PtScore.get_max_score(scores)
        min_score = PtScore.get_min_score(scores)
        avg_score = PtScore.get_avg_total_score(scores)

        avg_pushups = PtScore.get_avg_pushups(scores)
        avg_situps = PtScore.get_avg_situps(scores)
        avg_two_mile = PtScore.get_avg_run_time(scores)

        avg_pushup_score = PtScore.get_avg_pushup_score(scores)
        avg_situp_score = PtScore.get_avg_situp_score(scores)
        avg_two_mile_score = PtScore.get_avg_run_score(scores)

        context.update({
            'scores': scores,
            'ordered_scores': ordered_scores,
            'max_score': max_score,
            'min_score': min_score,
            'avg_score': avg_score,
            'avg_pushups': avg_pushups,
            'avg_situps': avg_situps,
            'avg_two_mile': avg_two_mile,
            'avg_pushup_score': avg_pushup_score,
            'avg_situp_score': avg_situp_score,
            'avg_two_mile_score': avg_two_mile_score,
        })

    #on request post, check if the user is cadre or not to determine whether the EditCadetFull and EditCadetUser
    # forms should be used, or just the more simple EditCadet form
    if request.method == 'POST':
        #if the cadet is cadre/superuser submitting form or user_form
        if hasattr(request.user, 'cadre') or request.user.is_superuser:
            form = EditCadetFull(request.POST or None, instance=cadet)
            user_form = EditCadetUser(request.POST or None, instance=cadet.user)
            if user_form.is_valid():
                user_form.save()
        #If the user is not cadre/superuser (does not include the user_form)
        else:
            form = EditCadet(request.POST or None, instance=cadet)

        if form.is_valid():
            form.save()

    elif request.method == "GET":
        if hasattr(request.user, 'cadre') or request.user.is_superuser:
            form = EditCadetFull(instance=cadet)
            user_form = EditCadetUser(instance=cadet.user)

        else:
            form = EditCadet(instance=cadet)

    context.update({'form': form, 'user_form': user_form})

    return render(request, template_name, context)


class AddCompany(View):
    template = 'personnel/company_pages/company_form.html'

    def post(self, request):
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('company_listing'))

    def get(self, request):
        form = AddCompanyForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)


class EditCompany(View):
    template = 'personnel/company_pages/company_form.html'

    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        form = EditCompanyForm(instance=company)

        platoons = company.platoons.all()

        context = {
            'company': company,
            'platoons': platoons,
            'form': form,
            'edit': True
        }
        return render(request, self.template, context)

    def post(self, request, company_id):
        company = Company.objects.get(id=company_id)
        form = EditCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('company_listing'))


class DeleteCompany(View):
    template = 'personnel/companies/delete.html'

    def post(self, request, company_id):
        company = Company.objects.get(id=company_id)
        company.delete()
        return HttpResponseRedirect(reverse('company_listing'))


def company_listing(request):
    template_name = 'personnel/company_pages/company_listing.html'

    companies = Company.objects.all()
    assigned_cadets = Cadet.objects.filter(company__isnull=False)
    unassigned_cadets = Cadet.objects.filter(company__isnull=True)

    context = {
        'companies': companies,
        'assigned_cadets': assigned_cadets,
        'unassigned_cadets': unassigned_cadets
    }

    return render(request, template_name, context)


class CompanyCadetListing(View):
    template_name = 'personnel/company_pages/company_cadet_listing.html'

    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        cadets = Cadet.objects.filter(company=company)
        return render(request, self.template_name, {'company': company, 'cadets': cadets})


class MSlevelListing(View):
    template_name = 'personnel/ms_listing.html'

    ms_classes = MsLevel.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'ms_classes': self.ms_classes})


class MScadetListing(View):
    template_name = 'personnel/ms_cadet_listing.html'

    def get(self, request, ms_class_id):
        ms_class = MsLevel.objects.get(id=ms_class_id)
        cadets = Cadet.objects.filter(ms_level=ms_class)
        return render(request, self.template_name, {'ms_class': ms_class, 'cadets': cadets})


class GroupingDetail(View):
    template = 'personnel/group_pages/grouping_profile.html'

    @staticmethod
    def get_grouping(grouping_type, id):
        if grouping_type == "companies":
            return Company.objects.get(id=id)
        elif grouping_type == "platoons":
            return Platoon.objects.get(id=id)
        elif grouping_type == "squads":
            return Squad.objects.get(id=id)
        elif grouping_type == "ms-classes":
            return MsLevel.objects.get(id=id)

    def get(self, request, grouping_id, grouping_type, tab="stats"):
        group = GroupingDetail.get_grouping(grouping_type, grouping_id)
        sub_groups = group.get_sub_groupings()
        sub_cadets = group.get_sub_cadets()

        context = {
            'tab': tab,
            'group': group,
            'sub_groupings': sub_groups,
            'sub_cadets': sub_cadets
        }

        context.update(grouping_data(sub_cadets))

        return render(request, self.template, context)


class Search(View):
    template = 'search/search_popup.html'

    def get(self, request, query_string):
        cadet_results = Cadet.objects.search(query_string, 'Cadet')
        company_results = Company.objects.search(query_string, 'Company')
        ms_level_results = MsLevel.objects.search(query_string, 'MS')
        context = {
            'query_string': query_string,
            'cadet_results': cadet_results,
            'company_results': company_results,
            'ms_level_results': ms_level_results
        }
        return render(request, self.template, context)


class Input(View):
    template = 'personnel/input_pages/personnel_input.html'

    def get(self, request):
        context = {}

        return render(request, self.template, context)

# TODO this is pretty nasty code... thrown together pretty quickly. Can use a rewrite sometime soon
# needs converting to a formset
class Organize(View):
    template = 'personnel/command_management/organize_staff.html'

    chain = assemble_staff_hierarchy()
    context = {
        'chain': chain
    }

    def get(self, request):
        return render(request, self.template, self.context)

    def post(self, request):
        form = CompanyStaffForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            commander = form.cleaned_data['commander']
            commander_new_squad = form.cleaned_data['commander_new_squad']
            company.company_commander.set_squad(commander_new_squad, commit=True)
            company.set_commander(commander)

            chain = assemble_staff_hierarchy()
            self.context['chain'] = chain
        else:
            pass
            # self.context['form'] = form

        return render(request, self.template, self.context)


def render_dd_js(request):
    template = 'personnel/command_management/js/command_management.js'
    chain = assemble_staff_hierarchy()

    context = {
        'chain': chain
    }

    return render(request, template, context)