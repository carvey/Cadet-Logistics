from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from pt.models import PtTest, PtScore, Grader
from personnel.models import Company, Cadet, MsLevel
from pt_utils import get_complete_average_scores_dict, get_avg_scores_by_company
from pt.forms import *

import json

class TestProfiletView(View):
    template_name = 'pt/pt_tests/test_profile.html'

    #each tab after stats (the first one) uses ajax to load
    def get(self, request, test_id, tab='stats'):
        context = {}
        test = PtTest.filtered_tests.get(id=test_id)
        #pagewide context
        context.update(
            {'test': test, 'tab': tab}
        )

        if tab == 'stats':
            top_scores = test.get_n_highest_scores(n=10)

            #this filter expression will be passed to the get_n_hightest_scores method to further filter scores
            filter_expression = {'cadet__contracted': False}
            top_non_contracted_scores = test.get_n_highest_scores(filter_expression=filter_expression, n=10)

            context.update({'top_scores': top_scores,
                            'top_non_contracted_scores': top_non_contracted_scores
            })

            top_squads = test.get_n_highest_squads()
            top_platoons = test.get_n_highest_platoons()

            filter_expression = {'pt_test': test}
            context.update(get_complete_average_scores_dict(filter_expression))
            context.update({'top_squads': top_squads, 'top_platoons': top_platoons})

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
    template = 'pt/pt_tests/test_form.html'

    def post(self, request):
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test_form.save()
        return HttpResponseRedirect(reverse("pt-tests-listing"))

    def get(self, request):
        test_form = TestForm()
        context = {'test_form': test_form}
        return render(request, self.template, context)


class EditTest(View):
    template = 'pt/pt_tests/test_form.html'

    def post(self, request, test_id):
        test = PtTest.future_tests.get(id=test_id)
        form = TestForm(request.POST, instance=test)
        context = {}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pt/tests/')
        else:
            context.update({'test_form': form})
            return render(request, self.template, context)

    def get(self, request, test_id):
        test = PtTest.future_tests.get(id=test_id)
        form = TestForm(instance=test)
        context = {'test_form': form, 'edit': True}
        return render(request, self.template, context)


# TODO: Would be nice to have suggesstions on misspelled cadet names for the error message. Fuzzywuzzy on github might be good for this
class InputTestScores(View):
    template = 'pt/pt_tests/add_scores.html'

    score_formset = formset_factory(ScoreForm, extra=2, can_delete=True)

    def post(self, request, test_id):
        formset = self.score_formset(request.POST, request.FILES)
        test = PtTest.objects.get(id=test_id)
        filtered_cadets = self.get_cadets(test)

        if formset.is_valid():
            for form in formset.cleaned_data:
                # Empty rows are sent back as an empty dict, so these can be skipped
                if form and not form.get('DELETE'):
                    cadet = Cadet.objects.get(id=int(form.get('cadet_id')))
                    try:
                        # if a score for this cadet has already been submitted for this test
                        score = PtScore.objects.get(pt_test=test, cadet=cadet)
                    except ObjectDoesNotExist:
                        # if this is the first time a score is being created for this cadet for this test
                        score = PtScore()
                    score.pt_test = test
                    score.cadet = cadet
                    score.pushups = form['pushups']
                    score.situps = form['situps']
                    score.two_mile = form['two_mile']
                    score.save()

            return HttpResponseRedirect('/pt/tests')
        else:
            context = {
                'test': test,
                'score_formset': formset,
                'filtered_cadets': filtered_cadets
            }
            return render(request, self.template, context)

    def get(self, request, test_id):
        test = PtTest.objects.get(id=test_id)
        filtered_cadets = self.get_cadets(test)

        context={
            'test': test,
            'score_formset': self.score_formset,
            'filtered_cadets': filtered_cadets
        }
        return render(request, self.template, context)

    @staticmethod
    def get_cadets(test):
        test_levels = [x for x in test.ms_levels.all()]
        filtered_cadets = Cadet.objects.filter(ms_level__in=test_levels)
        # commenting filtered auto-suggestions out until a better way to pass cadet id's in the form can be worked out
        # scores = test.ptscore_set.all()
        # scores = [score.cadet.id for score in scores]
        # filtered_cadets = filtered_cadets.exclude(id__in=scores)
        return filtered_cadets


def calculate_score(request, cadet_id, situps, pushups, two_mile):
    """
    A view to be used with ajax to calculate pt scores as they are being entered
    :param request:
    :return:
    """
    score = PtScore.calculate_score(cadet_id=cadet_id, raw_situps=situps, raw_pushups=pushups, run_time=two_mile)
    return HttpResponse(json.dumps(score), content_type='application/json')


class TestListingView(View):
    template_name = 'pt/pt_tests/test_listing.html'

    def get(self, request):
        pt_tests = PtTest.filtered_tests.all().order_by('-date')
        future_tests = PtTest.future_tests.all().order_by('date')
        context = {
            'future_tests': future_tests,
            'tests': pt_tests,
        }
        return render(request, self.template_name, context)


class TestScoresView(View):
    template_name = "pt/pt_tests/scores_by_test.html"

    def get(self, request, test_id):
        cadets = Cadet.objects.all()
        test = PtTest.filtered_tests.get(id=test_id)
        scores = PtScore.objects.filter(pt_test=test)
        context = {
            'scores': scores,
            'cadets': cadets,
        }
        return render(request, self.template_name, context)


class StatisticsView(View):
    template_name = 'pt/stat_page/statistics.html'
    # TODO: If a cadet isn't in an ms level taking the pt_test, they should not be taken into account for the test in any way

    def get(self, request, tab='cadets'):
        avg_pt_scores = {}
        pt_tests = PtTest.filtered_tests.all()

        for test_counter, pt_test in enumerate(pt_tests):
            pt_scores = PtScore.objects.filter(pt_test=pt_test)
            total_num = len(pt_scores)
            avg_score = 0
            if total_num:
                total_score = 0
                for score_counter, pt_score in enumerate(pt_scores):
                    total_score += pt_score.score
                avg_score = float(total_score)/total_num

            avg_pt_scores[pt_test] = avg_score

        #This is to get the avg scores per company per pt test
        test_scores = {}
        for company in Company.objects.all():
            test_dict = {}
            for test in PtTest.filtered_tests.all():
                avg = test.get_average_score(company)
                test_dict.update({test: avg})
            test_scores[company] = test_dict

        pushups = {}
        situps = {}
        run = {}
        for test in PtTest.filtered_tests.all():
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