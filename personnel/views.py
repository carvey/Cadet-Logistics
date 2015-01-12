from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from personnel.models import Cadet, Company, MsLevel, Platoon, SnapShot, Demographic
from pt.models import PtScore, PtTest, Grader
from personnel_utils import grouping_data
from django.contrib.auth.decorators import login_required
from personnel.forms import LoginForm

# Create your views here.


class Login(FormView):
    template_name = 'auth/login.html'
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

class Index(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name, {})


class Stats(View):
    template_name = 'personnel/stat_page/personnel_stats.html'

    def get(self, request, tab='cadets'):
        cadets = Cadet.objects.all()
        current_cadets = cadets.filter(commissioned=False, dropped=False)
        nursing_contracted = cadets.filter(nurse_contracted=True)
        demographics = Demographic.objects.all()

        snapshots = SnapShot.objects.all()

        demo_dict = {}
        for demo in demographics:
            demo_dict[demo.demographic] = 0

        for cadet in cadets:
            if cadet.demographic:
                demo_dict[cadet.demographic.demographic] += 1



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


class CadetPage(View):
    template_name = 'personnel/cadet_page/cadet_page.html'

    def get(self, request, cadet_id, tab='overview'):
        cadet = Cadet.objects.get(id=cadet_id)
        scores = PtScore.objects.filter(cadet=cadet_id)
        ordered_scores = scores.order_by('-pt_test')[:3]

        # initializing pt related vars to 0 ahead of time, in case the cadet has no pt tests yet
        max_score = min_score = avg_score = avg_pushups = avg_situps = avg_two_mile = 0
        avg_pushup_score = avg_situp_score = avg_two_mile_score = 0


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

        context = {
            'cadet': cadet,
            'scores': ordered_scores,
            'max_score': max_score,
            'min_score': min_score,
            'avg_score': avg_score,
            'avg_pushups': avg_pushups,
            'avg_situps': avg_situps,
            'avg_two_mile': avg_two_mile,
            'avg_pushup_score': avg_pushup_score,
            'avg_situp_score': avg_situp_score,
            'avg_two_mile_score': avg_two_mile_score,
            'tab': tab,
        }
        return render(request, self.template_name, context)


class CompanyDetail(View):
    template = 'personnel/group_pages/grouping_profile.html'

    def get(self, request, company_name, tab='stats'):
        company = Company.objects.get(name=company_name)
        group = "%s Company" % company.name
        groups = Platoon.objects.filter(company=company)
        link = "platoons"
        listing_template = 'personnel/group_pages/company_datatable_listing.html'

        context = {'tab': tab,
                   'company': company,
                   'group': group,
                   'groups': groups,
                   'link': link,
                   'listing_template': listing_template,
                   }

        #Additions to the context
        cadets = Cadet.objects.filter(company=company)
        context.update(grouping_data(cadets))

        return render(request, self.template, context)


class CompanyListing(View):
    template_name = 'personnel/company_listing.html'

    companies = Company.objects.all()
    platoons = Platoon.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'companies': self.companies, 'platoons': self.platoons})


class CompanyCadetListing(View):
    template_name = 'personnel/company_cadet_listing.html'

    def get(self, request, company_name):
        company = Company.objects.get(name=company_name)
        cadets = Cadet.objects.filter(company=company)
        return render(request, self.template_name, {'company': company, 'cadets': cadets})


class MSLevelDetail(View):
    template = 'personnel/group_pages/grouping_profile.html'

    def get(self, request, ms_class, tab='stats'):
        ms_level = MsLevel.objects.get(name=ms_class)
        group = "%s Class" % ms_level.name
        groups = Cadet.objects.filter(ms_level=ms_level)
        link = "/personnel/cadets"
        listing_template = 'personnel/group_pages/grouping_listing.html'

        context = {'tab': tab,
                   'group': group,
                   'groups': groups,
                   'link': link,
                   'listing_template': listing_template,
                   }
        cadets = Cadet.objects.filter(ms_level=ms_level)
        context.update(grouping_data(cadets))

        return render(request, self.template, context)


class MSlevelListing(View):
    template_name = 'personnel/ms_listing.html'

    ms_classes = MsLevel.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'ms_classes': self.ms_classes})


class MScadetListing(View):
    template_name = 'personnel/ms_cadet_listing.html'

    def get(self, request, ms_class):
        ms_class = MsLevel.objects.get(name=ms_class)
        cadets = Cadet.objects.filter(ms_level=ms_class)
        return render(request, self.template_name, {'ms_class': ms_class, 'cadets': cadets})


class PlatoonDetail(View):
    template = 'personnel/group_pages/grouping_profile.html'

    def get(self, request, company_name, platoon_id, tab='stats'):
        company = Company.objects.get(name=company_name)
        platoon = Platoon.objects.get(id=platoon_id, company=company)
        group = "%s Platoon" % platoon.name
        groups = Cadet.objects.filter(platoon=platoon)
        link = "/personnel/cadets"
        listing_template = 'personnel/group_pages/grouping_listing.html'

        context = {'tab': tab,
                   'platoon': platoon,
                   'group': group,
                   'groups': groups,
                   'link': link,
                   'listing_template': listing_template,
                   }
        #Additons to the context
        cadets = Cadet.objects.filter(platoon=platoon)
        context.update(grouping_data(cadets))

        return render(request, self.template, context)


class PlatoonListing(View):
    template = ''

    def get(self, request):
        return render(request, self.template, {})