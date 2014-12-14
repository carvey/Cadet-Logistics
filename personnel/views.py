from django.shortcuts import render
from django.views.generic import View
from personnel.models import Cadet, Company, MsLevel, Platoon, SnapShot, Demographic
from pt.models import PtScore, PtTest, Grader
import collections

# Create your views here.


class Index(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name, {})

class Stats(View):
    template_name = 'personnel/personnel_stats.html'

    def get(self, request, tab='cadets'):
        cadets = Cadet.objects.all()
        current_cadets = cadets.filter(commissioned=False, dropped=False)
        at_risk_cadets = cadets.filter(at_risk=True)
        contracted_cadets = cadets.filter(contracted=True)
        smp_cadets = cadets.filter(contracted=True)
        nursing_contracted = cadets.filter(nurse_contracted=True)
        demographics = Demographic.objects.all()

        snapshots = SnapShot.objects.all()

        male_cadets = cadets.filter(gender='male')
        female_cadets = cadets.filter(gender='female')

        demo_dict = {}
        for demo in demographics:
            demo_dict[demo.demographic] = 0

        for cadet in cadets:
            if cadet.demographic:
                demo_dict[cadet.demographic.demographic] += 1

        avg_gpa = Cadet.get_avg_gpa(current_cadets)
        completed_volunteer_hours = len(cadets.filter(volunteer_hours_status=True))
        not_completed_volunteer_hours = len(cadets.exclude(volunteer_hours_status=True))

        context = {
            'tab': tab,
            'snapshots': snapshots,
            'cadets': current_cadets,
            'at_risk_cadets': at_risk_cadets,
            'contracted_cadets': contracted_cadets,
            'nursing_contracted': nursing_contracted,
            'demographics': demo_dict,
            'smp_cadets': smp_cadets,
            'male_cadets': male_cadets,
            'female_cadets': female_cadets,
            'avg_gpa': avg_gpa,
            'volunteer_hours': completed_volunteer_hours,
            'not_volunteer_hours': not_completed_volunteer_hours,
        }

        return render(request, self.template_name, context)


class CadetListing(View):
    template_name = 'personnel/cadet_listing.html'

    cadets = Cadet.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'cadets': self.cadets})


class CadetPage(View):
    template_name = 'personnel/cadet_page.html'

    def get(self, request, cadet_id, tab='overview'):
        cadet = Cadet.objects.get(id=cadet_id)
        scores = PtScore.objects.filter(cadet=cadet_id)
        ordered_scores = scores.order_by('-pt_test')[:3]
        score_values = Grader.objects.all()

        # initializing pt related vars to 0 ahead of time, in case the cadet has no pt tests yet
        max_score = min_score = avg_score = avg_pushups = avg_situps = avg_two_mile = 0
        avg_pushup_score = avg_situp_score = avg_two_mile_score = 0

        ptscore = PtScore()

        if scores:
            max_score = ptscore.get_max_score(scores)
            min_score = ptscore.get_min_score(scores)
            avg_score = ptscore.get_avg_total_score(scores)

            avg_pushups = ptscore.get_avg_pushups(scores)
            avg_situps = ptscore.get_avg_situps(scores)
            avg_two_mile = ptscore.get_avg_run_time(scores)

            avg_pushup_score = ptscore.get_avg_pushup_score(cadet, scores)
            avg_situp_score = ptscore.get_avg_situp_score(cadet, scores)
            avg_two_mile_score = ptscore.get_avg_run_score(cadet, scores)

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
    template = 'personnel/grouping_profile.html'

    def get(self, request, company_name, tab='stats'):
        company = Company.objects.get(name=company_name)
        group = "%s Company" % company.name
        groups = Platoon.objects.filter(company=company)
        link = "platoons"
        listing_template = 'personnel/grouping_listing.html'

        cadets = Cadet.objects.filter(company=company)
        count = cadets.count()
        contracted = cadets.filter(contracted=True)
        smp = cadets.filter(smp=True)
        avg_gpa = Cadet.get_avg_gpa(cadets)
        at_risk = cadets.filter(at_risk=True)
        profiles = cadets.filter(on_profile=True)
        # test = PtTest.objects.all().order_by('-id')[0]
        # scores = PtScore.objects.filter(pt_test=test)
        #top_pt_cadets = test.get_n_highest_scores(cadets, scores, 3)

        #Get the top 3 cadets
        all_scores = PtScore.objects.all()
        avg_scores = {}
        ptscore = PtScore()
        for cadet in cadets:
            scores = all_scores.filter(cadet=cadet)
            avg_scores[cadet] = ptscore.get_avg_total_score(scores)
        avg_scores = collections.OrderedDict(reversed(sorted(avg_scores.items(), key=lambda t: t[1])))
        top_scores = collections.OrderedDict()
        count = 0
        for x, y in avg_scores.items():
            top_scores.update({x: y})
            count += 1
            if count > 3: #the number of top cadets to get
                break

        context = {'tab': tab,
                   'cadets': cadets,
                   'company': company,
                   'group': group,
                   'groups': groups,
                   'link': link,
                   'listing_template': listing_template,
                   'contracted': contracted,
                   'smp': smp,
                   'avg_gpa': avg_gpa,
                   'at_risk': at_risk,
                   'profiles': profiles,
                   'top_scores': top_scores,

                   }
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
    template = 'personnel/grouping_profile.html'

    def get(self, request, ms_class, tab='stats'):
        ms_level = MsLevel.objects.get(name=ms_class)
        group = "%s Class" % ms_level.name
        groups = Cadet.objects.filter(ms_level=ms_level)
        link = "/personnel/cadets"
        listing_template = 'personnel/grouping_listing.html'

        context = {'tab': tab,
                   'group': group,
                   'groups': groups,
                   'link': link,
                   'listing_template': listing_template,
                   }
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
    template = 'personnel/grouping_profile.html'

    def get(self, request, company_name, platoon_id, tab='stats'):
        company = Company.objects.get(name=company_name)
        platoon = Platoon.objects.get(id=platoon_id, company=company)
        group = "%s Platoon" % platoon.name
        groups = Cadet.objects.filter(platoon=platoon)
        link = "/personnel/cadets"
        listing_template = 'personnel/grouping_listing.html'

        context = {'tab': tab,
                   'platoon': platoon,
                   'group': group,
                   'groups': groups,
                   'link': link,
                   'listing_template': listing_template,
                   }
        return render(request, self.template, context)


class PlatoonListing(View):
    template = ''

    def get(self, request):
        return render(request, self.template, {})