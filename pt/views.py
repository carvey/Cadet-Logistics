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
from pt.pt_utils.utils import get_complete_average_scores_dict, get_avg_scores_by_company
from pt.forms import *

import json
from decimal import Decimal


class TestProfiletView(View):
    template_name = 'pt/pt_tests/test_profile.html'

    def get(self, request, test_id, tab='stats'):
        #TODO changed FilteredTests to objects for the time being. Need to change this back possibly?
        test = PtTest.objects.get(id=test_id)
        top_scores = test.get_n_highest_scores(n=10)

        #this filter expression will be passed to the get_n_hightest_scores method to further filter scores
        filter_expression = {'cadet__contracted': False}
        top_non_contracted_scores = test.get_n_highest_scores(filter_expression=filter_expression, n=10)

        top_squads = test.get_n_highest_squads()
        top_platoons = test.get_n_highest_platoons()

        filter_expression = {'pt_test': test}

        cadets = Cadet.objects.all()
        scores = PtScore.objects.filter(pt_test=test)

        context = {
            'scores': scores,
            'cadets': cadets,
            'test': test,
            'tab': tab,
            'top_squads': top_squads,
            'top_platoons': top_platoons,
            'top_scores': top_scores,
            'top_non_contracted_scores': top_non_contracted_scores
        }

        context.update(get_complete_average_scores_dict(filter_expression))
        return render(request, self.template_name, context)


class AddTest(View):
    template = 'pt/pt_tests/test_form.html'

    def post(self, request):
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test_form.save()
        else:
            return self.get(request, test_form)
        return HttpResponseRedirect(reverse("pt-tests-listing"))

    def get(self, request, form=None):
        if form:
            test_form = form
        else:
            test_form = TestForm()
        context = {'test_form': test_form}
        return render(request, self.template, context)


class EditTest(View):
    template = 'pt/pt_tests/test_form.html'

    def post(self, request, test_id):
        test = PtTest.objects.get(id=test_id)
        form = TestForm(request.POST, instance=test)
        context = {}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pt/tests/')
        else:
            context.update({'test_form': form})
            return render(request, self.template, context)

    def get(self, request, test_id):
        test = PtTest.objects.get(id=test_id)
        form = TestForm(instance=test)
        context = {'test_form': form, 'edit': True}
        return render(request, self.template, context)


class DeleteTest(View):

    # TODO this should be changed to post
    def get(self, request, test_id):
        test = PtTest.objects.get(id=test_id)
        test.ptscore_set.all().delete()
        test.delete()
        return HttpResponseRedirect(reverse('pt-tests-listing'))


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


def calculate_score(request, situps, pushups, two_mile, cadet_id=None, gender=None, age=None):
    """
    A view to be used with ajax to calculate pt scores as they are being entered
    :param request:
    :return:
    """
    if age and gender:
        instance = PtScore.assemble_minimal_instance(age, gender, situps, pushups, two_mile)
    else:
        test_id = request.GET['test_id']
        instance = PtScore.assemble_instance(cadet_id=cadet_id, test_id=test_id, raw_situps=situps, raw_pushups=pushups, run_time=two_mile)
    score = PtScore.calculate_score(instance)
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
            avg = 0
            test_dict = {}
            for test in PtTest.filtered_tests.all():
                avg = test.get_average_score(company)
                if avg:
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

        batallion_averages = {}
        score_sum = 0
        contracted_average = 0
        non_contracted_average = 0
        scores = PtScore.objects.all()
        contracted_count = 0
        non_contracted_count = 0
        for score in scores:
            score_sum += score.score
            if score.cadet.contracted:
                contracted_count += 1
                contracted_average += score.score
            else:
                non_contracted_count += 1
                non_contracted_average += score.score

        if scores:
            batallion_averages.update({
                'score': (Decimal(score_sum) / Decimal(scores.count())).quantize(Decimal(10) ** -2),
                'contracted':(Decimal(contracted_average) / Decimal(contracted_count)).quantize(Decimal(10) ** -2),
                'non_contracted': (Decimal(non_contracted_average) / Decimal(non_contracted_count)).quantize(Decimal(10) ** -2)
            })

        context = {
            'tab': tab,
            'data': avg_pt_scores,
            'company_scores': test_scores,
            'pushup_test_scores': pushups,
            'situp_test_scores': situps,
            'run_test_scores': run,
            'top_cadets': top_cadets,
            'batallion_averages': batallion_averages
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

        score_dict = {}
        for cadet in cadets:
            scores = all_scores.filter(cadet=cadet)

            avg_pushup_scores = PtScore.get_avg_pushup_score(scores)
            avg_pushups = PtScore.get_avg_pushups(scores)
            pushups = {'raw': avg_pushups, 'score': avg_pushup_scores}

            avg_situp_scores = PtScore.get_avg_situp_score(scores)
            avg_situps = PtScore.get_avg_situps(scores)
            situps = {'raw': avg_situps, 'score': avg_situp_scores}

            avg_run_scores = PtScore.get_avg_run_score(scores)
            avg_run_time = PtScore.get_avg_run_time(scores)
            run = {'raw': avg_run_time, 'score': avg_run_scores}

            avg_scores = PtScore.get_avg_total_score(scores)

            score_dict.update({cadet: {'pushups': pushups, 'situps': situps, 'run': run, 'total': avg_scores}})

        context = {
            'cadets': cadets,
            'score_dict': score_dict
        }
        return render(request, self.template_name, context)


class PTInfo(View):
    template = 'pt/input_pages/pt_input.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)


class PTCalculator(View):
    template = 'pt/input_pages/calculator.html'

    def get(self, request):
        form = ScoreCalculatorForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)