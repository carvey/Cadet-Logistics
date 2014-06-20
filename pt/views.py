from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from pt.models import PtTest, PtScore
from eagletrack.models import Company

class Dashboard(View):
    '''
    Creates a dictionary of all the pt scores for each company. Accessed using company name.
    '''
    def company_pt_scores():
        companies = Company.objects.all()
        scores_by_company = {}
        for company in companies:
            scores = PtScore.objects.filter(cadet__company=company)
            avg_score = {}
            
            avg_score['situps'] = sum([score.get_situps() for score in scores]) / (len([score.get_situps() for score in scores]))
            avg_score['pushups'] = sum([score.get_pushups() for score in scores]) / float(len([score.get_pushups() for score in scores]))
            avg_score['two_mile'] = sum([score.get_two_mile_min() for score in scores]) / float(len([score.get_two_mile_min() for score in scores]))
            
            scores_by_company[company.name] = avg_score
        
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
        
    def avg_company_scores(self):
        pass

class CpView(View):
    template_name = 'pt/control_panel.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT CP")
    
class TestView(View):
    emplate_name = 'pt/tests.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT Tests")

class CadetsView(View):
    template_name = 'pt/cadets.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT Cadets page.")

class CompanyView(View):
    template_name = 'pt/company.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT company page")
    
class MsLevelView(View):
    template_name = 'pt/ms_level.html'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("PT mslevel page")