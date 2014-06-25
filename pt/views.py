from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from pt.models import PtTest, PtScore
from eagletrack.models import Company

'''
Returns a dictionary containing the average values of situps, pushups and two mile run times
for the given Company object.
Ex.
    To access the average situp value from the returned dictionary, you would do <dict_name>['situps']
'''    
def get_avg_scores_by_company(company):
    try:
        scores = PtScore.objects.filter(cadet__company=company)
        avg_score = {}
        
        situps = [score.get_situps() for score in scores]
        avg_situps = sum(situps)/float(len(situps))
        
        pushups = [score.get_pushups() for score in scores]
        avg_pushups = sum(pushups)/float(len(pushups))
        
        two_mile = [score.get_two_mile_min() for score in scores]
        avg_two_mile = sum(two_mile)/float(len(two_mile))
    
        return {
                'situps':avg_situps,
                'pushups':avg_pushups,
                'two_mile':avg_two_mile
                }
    except:
        pass
    
class Dashboard(View):
    '''
    Creates a dictionary of all the pt scores for each company. Accessed using company name.
    '''
    def company_pt_scores():
        companies = Company.objects.all()
        scores_by_company = {}
        for company in companies:
            scores_by_company[company.name] = get_avg_scores_by_company(company)
        
        print scores_by_company
        return scores_by_company
    
    template_name = 'pt/dashboard.html'
    
    pt_tests = PtTest.objects.all()
    pt_scores = PtScore.objects.all()
    scores_by_company = company_pt_scores()
    companies = Company.objects.all()

    context = {
               'tests':pt_tests,
               'companies':companies,
               'company_scores':scores_by_company,
               }
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

class CpView(View):
    template_name = 'pt/control_panel.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT CP")
    
class TestView(View):
    template_name = 'pt/tests.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT Tests")
    
class TestStatView(View):
    template_name = 'pt/test_stats.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT test statistics view")
    
class TestListingView(View):
    template_name = 'pt/test_listing.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT listing view")

class CadetsView(View):
    template_name = 'pt/cadets.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT Cadets page.")
    
class CadetsStatView(View):
    template_name = 'pt/cadets_stats.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("Cadets PT Statistics page.")

class CadetsListingView(View):
    template_name = 'pt/cadets_listing.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("Cadets PT listing page.")

class CompanyView(View):
    template_name = 'pt/company.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT company page")
    
class MsLevelView(View):
    template_name = 'pt/ms_level.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT mslevel page")