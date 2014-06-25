from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from pt.models import PtTest, PtScore
from personnel.models import Company, Cadet

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
    
        return scores_by_company
        try:
            companies = Company.objects.all()
            scores_by_company = {}
            for company in companies:
                scores_by_company[company.name] = get_avg_scores_by_company(company)
            
            return scores_by_company
        except:
            return None
    
    template_name = 'pt/dashboard.html'
    
    def get(self, request):
        pt_tests = PtTest.objects.all()
        pt_scores = PtScore.objects.all()
        scores_by_company = company_pt_scores()
        companies = Company.objects.all()
    
        context = {
                   'tests':pt_tests,
                   'companies':companies,
                   'company_scores':scores_by_company,
                   }
    
        return render(request, self.template_name, context)

class CpView(View):
    template_name = 'pt/control_panel.html'
    
    def get(self, request):
        context = {
                  }
        return render(request, self.template_name, context)
    
class TestView(View):
    template_name = 'pt/tests.html'
    
    def get(self, request):
        context = {
                   }
        return render(request, self.template_name, context)
    
class TestStatView(View):
    template_name = 'pt/test_stats.html'
    
    def get(self, request):
        context = {
                   }
        return render(request, self.template_name, context)
    
class TestListingView(View):
    template_name = 'pt/test_listing.html'
    
    def get(self, request):
        pt_scores = PtScore.objects.all()
        context = {
                   'scores':pt_scores,
                   }
        return render(request, self.template_name, context)
    
class CadetDetailView(View):
    template_name = 'pt/cadet_detail.html'
    
    def get(self, request, cadet_id):
        scores = PtScore.objects.filter(cadet__id=cadet_id)
        cadet = Cadet.objects.filter(id=cadet_id)
        context = {
                   'cadet':cadet[0],
                   'scores':scores
                   }
        return render(request, self.template_name, context)

class CadetsView(View):
    template_name = 'pt/cadets.html'
    
    def get(self, request):
        context = {
                   }
        return render(request, self.template_name, context)
    
class CadetsStatView(View):
    template_name = 'pt/cadets_stats.html'
    
    def get(self, request):
        context = {
                   }
        return render(request, self.template_name, context)

class CadetsListingView(View):
    template_name = 'pt/cadets_listing.html'
    
    def get(self, request):
        cadets = Cadet.objects.all()
        context = {
                   'cadets':cadets
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
