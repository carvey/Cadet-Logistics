from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q
from django.core.urlresolvers import reverse

from pt.models import PtTest, PtScore, Grader
from personnel.models import Company, Cadet
from pt_utils import get_complete_average_scores_dict, get_avg_scores_by_company
from pt.forms import *


class TestProfiletView(View):
    template_name = 'pt/pt_tests/test_profile.html'

    #each tab after stats (the first one) uses ajax to load
    def get(self, request, test_id, tab='stats'):
        context = {}
        test = PtTest.objects.get(id=test_id)
        #sitewide context
        context.update(
            {'test': test, 'tab': tab}
        )

        if tab == 'stats':
            top_scores = test.get_n_highest_scores(n=5)

            filter_expression = {'cadet__contracted': False}
            top_non_contracted_scores = test.get_n_highest_scores(filter_expression=filter_expression, n=5)

            context.update({'top_scores': top_scores,
                            'top_non_contracted_scores': top_non_contracted_scores
            })

            filter_expression = {'pt_test': test}
            context.update(get_complete_average_scores_dict(filter_expression))
            return render(request, self.template_name, context)

        elif tab == 'listing':
            template_name = 'pt/pt_tests/test_profile_listing.html'
            cadets = Cadet.objects.all()
            scores = PtScore.objects.filter(pt_test=test)
            context.update({
                'scores': scores,
                'cadets': cadets,
            })
            return render(request, template_name, context)

        return render(request, self.template_name, context)


class AddTest(View):
    template = 'pt/pt_tests/add_test.html'

    def post(self, request):
        test_form = AddTestForm(request.POST)
        if test_form.is_valid():
            test_form.save()
        return HttpResponseRedirect(reverse("pt-tests-listing"))

    def get(self, request):
        test_form = AddTestForm()

        context = {'test_form': test_form}
        return render(request, self.template, context)


class TestListingView(View):
    template_name = 'pt/pt_tests/test_listing.html'

    def get(self, request):
        pt_tests = PtTest.objects.all().order_by('-date')
        future_tests = PtTest.future_tests.all()
        context = {
            'future_tests': future_tests,
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

        #This is to get the avg scores per company per pt test
        test_scores = {}
        for company in Company.objects.all():
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
        }

        context.update(
            get_complete_average_scores_dict()
        )
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


class PTInfo(View):
    template = 'pt/input_pages/pt_input.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)