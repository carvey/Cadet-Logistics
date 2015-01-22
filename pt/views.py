from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q

from pt.models import PtTest, PtScore, Grader
from personnel.models import Company, Cadet
from pt_utils import get_complete_average_scores_dict, get_avg_scores_by_company


"""
Might be useful for in the future
---------
class Dashboard(View):
    template_name = 'pt/dashboard.html'
    
    '''
    Creates a dictionary of all the pt scores for each company. Accessed using company name.
    '''
    def company_pt_scores(self):
        companies = Company.objects.all()
        scores_by_company = {}
        for company in companies:
            scores_by_company[company.name] = get_avg_scores_by_company(company)
    
        return scores_by_company
        try:
            companies = Company.objects.all()
            scores_by_company = {}
            for company in companies:
                scores_by_company[company.name] = get_avg_scores_by_company(company)
            
            return scores_by_company
        except:
            return None
    
    def get(self, request):
        pt_tests = PtTest.objects.all()
        pt_scores = PtScore.objects.all()
        scores_by_company = self.company_pt_scores()
        companies = Company.objects.all()
    
        context = {
                   'tests':pt_tests,
                   'companies':companies,
                   'company_scores':scores_by_company,
                   }
    
        return render(request, self.template_name, context)
"""


class TestView(View):
    template_name = 'pt/tests.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class TestProfiletView(View):
    template_name = 'pt/test_profile/test_profile.html'

    #each tab after stats (the first one) uses ajax to load
    def get(self, request, test_id, tab='stats'):
        context = {}
        test = PtTest.objects.get(id=test_id)
        #sitewide context
        context.update(
            {'test': test, 'tab': tab}
        )

        if tab == 'stats':
            filter_expression = {'pt_test': test}
            context.update(
                get_complete_average_scores_dict(filter_expression)
            )
            return render(request, self.template_name, context)

        elif tab == 'listing':
            template_name = 'pt/test_profile/test_profile_listing.html'
            cadets = Cadet.objects.all()
            scores = PtScore.objects.filter(pt_test=test)
            context.update({
                'scores': scores,
                'cadets': cadets,
            })
            return render(request, template_name, context)

        return render(request, self.template_name, context)


class TestListingView(View):
    template_name = 'pt/test_listing.html'

    def get(self, request):
        pt_tests = PtTest.objects.all()
        context = {
            'tests': pt_tests,
        }
        return render(request, self.template_name, context)


class TestScoresView(View):
    template_name = "pt/scores_by_test.html"

    def get(self, request, test_id):
        cadets = Cadet.objects.all()
        test = PtTest.objects.get(id=test_id)
        scores = PtScore.objects.filter(pt_test=test)
        context = {
            'scores': scores,
            'cadets': cadets,
        }
        return render(request, self.template_name, context)


class CadetDetailView(View):
    template_name = 'pt/cadet_detail.html'

    def get(self, request, cadet_id):
        scores = PtScore.objects.filter(cadet__id=cadet_id)
        cadet = Cadet.objects.filter(id=cadet_id)
        context = {
            'cadet': cadet[0],
            'scores': scores
        }
        return render(request, self.template_name, context)


class CadetsView(View):
    template_name = 'pt/cadets.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class StatisticsView(View):
    template_name = 'pt/stat_page/statistics.html'

    def get(self, request, tab='cadets'):
        avg_pt_scores = {}
        pt_tests = PtTest.objects.all()

        for test_counter, pt_test in enumerate(pt_tests):
            pt_scores = PtScore.objects.filter(pt_test=pt_test)
            total_num = len(pt_scores)
            total_score = 0
            for score_counter, pt_score in enumerate(pt_scores):
                total_score += pt_score.score
            avg_score = float(total_score)/total_num
            avg_pt_scores[pt_test] = avg_score


        #most of the following code is used to get the average score for each pt event for each company
        #This block serves two purposes though. The other is to get the avg scores per company per pt test
        test_scores = {}
        avg_overall_scores = {}
        avg_pushup_scores = {}
        avg_situp_scores = {}
        avg_run_scores = {}
        for company in Company.objects.all():
            scores = PtScore.objects.filter(cadet__company=company)
            avg_overall_scores.update({company: PtScore.get_avg_total_score(scores)})
            avg_pushup_scores.update({company: PtScore.get_avg_pushup_score(scores)})
            avg_situp_scores.update({company: PtScore.get_avg_situp_score(scores)})
            avg_run_scores.update({company: PtScore.get_avg_run_score(scores)})
            #the following is used for getting the avg scores per company per pt test
            test_dict = {}
            for test in PtTest.objects.all():
                avg = test.get_average_score(company)
                test_dict.update({test: avg})
            test_scores[company] = test_dict
        pushups = {}
        situps = {}
        run = {}
        for test in PtTest.objects.all():
            scores = PtScore.objects.filter(pt_test=test)
            avg_pushup_score = PtScore.get_avg_pushup_score(scores)
            avg_situp_score = PtScore.get_avg_situp_score(scores)
            avg_run_score = PtScore.get_avg_run_score(scores)

            pushups.update({test: avg_pushup_score})
            situps.update({test: avg_situp_score})
            run.update({test: avg_run_score})

        cadets = Cadet.objects.all()
        top_cadets = PtScore.get_top_cadets(cadets)
        worst_cadets = PtScore.get_worst_cadets(cadets)

        context = {
            'tab': tab,
            'data': avg_pt_scores,
            'company_scores': test_scores,
            'pushup_test_scores': pushups,
            'situp_test_scores': situps,
            'run_test_scores': run,
            'top_cadets': top_cadets,
            'lowest_cadets': worst_cadets,
            'overall_scores': avg_overall_scores,
            'situp_scores': avg_situp_scores,
            'pushup_scores': avg_pushup_scores,
            'run_scores': avg_run_scores

        }
        return render(request, self.template_name, context)


class CadetsListingView(View):
    template_name = 'pt/cadets_listing.html'

    def get(self, request):
        cadets = Cadet.objects.all()
        all_scores = PtScore.objects.all()

        avg_pushup_scores = {}
        avg_situp_scores = {}
        avg_run_scores = {}
        avg_scores = {}

        ptscore = PtScore()

        for cadet in cadets:
            scores = all_scores.filter(cadet=cadet)

            avg_pushup_scores[cadet.id] = ptscore.get_avg_pushup_score(scores)
            avg_situp_scores[cadet.id] = ptscore.get_avg_situp_score(scores)
            avg_run_scores[cadet.id] = ptscore.get_avg_run_score(scores)
            avg_scores[cadet.id] = PtScore.get_avg_total_score(scores)

        context = {
            'cadets': cadets,
            'avg_pushup_scores': avg_pushup_scores,
            'avg_situp_scores': avg_situp_scores,
            'avg_run_scores': avg_run_scores,
            'avg_scores': avg_scores
        }
        return render(request, self.template_name, context)


class CompanyView(View):
    template_name = 'pt/company.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class CompanyStatView(View):
    template_name = 'pt/company_stats.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class CompanyListingView(View):
    template_name = 'pt/company_listing.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class MsLevelStatView(View):
    template_name = 'pt/ms_stats.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class MsLevelListingView(View):
    template_name = 'pt/ms_listing.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)


class MsLevelView(View):
    template_name = 'pt/ms_level.html'

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)
