from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import View

from personnel.models import Cadet, Company, MsLevel, Platoon
from pt.models import PtScore, Grader

# Create your views here.

class index(View):
    template_name = "index.html"
    def get(self, request):
        return render(request, self.template_name, {})
    
    
class CadetStats(View):
    template_name = 'personnel/cadet_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})

class CadetListing(View):
    template_name='personnel/cadet_listing.html'
    
    cadets = Cadet.objects.all()
    
    def get(self, request):
        return render (request, self.template_name, {'cadets': self.cadets})
    
class CadetPage(View):
    template_name='personnel/cadet_page.html'
    
    def get(self, request, cadet_id, tab='overview'):
        cadet = Cadet.objects.get(id = cadet_id)
        scores = PtScore.objects.filter(cadet = cadet_id)
        ordered_scores = scores.order_by('-pt_test')[:3]
        
        max_score = cadet.get_max_score(scores)
        avg_score = cadet.average_total_score(scores)
        
        #gets the age range that a cadet is a part of. Used for getting the correct Grader (score value) object
        def get_score_value_age_group(cadet):
            cadet_age = cadet.age
            score_values = Grader.objects.all()
            for score_value in score_values:
                value = score_value.age_group.split('-')
                if cadet_age >= int(value[0]) and cadet_age <= int(value[1]):
                    return score_value.age_group
                
        
        #queries for getting the Grader objects (score values)
        age = get_score_value_age_group(cadet)
        pushup_score_values = Grader.objects.get(gender=cadet.gender, activity='pushups', age_group=age).get_ordered_dict()
        situp_score_values = Grader.objects.get(gender=cadet.gender, activity='situps', age_group=age).get_ordered_dict() 
        two_mile_score_values = Grader.objects.get(gender=cadet.gender, activity='Two-mile run', age_group=age).get_ordered_dict()
        
        weakest_event = cadet.strongest_weakest_event(scores, pushup_score_values, situp_score_values, two_mile_score_values, "weak")
        strongest_event = cadet.strongest_weakest_event(scores, pushup_score_values, situp_score_values, two_mile_score_values, "strong")
                
        avg_pushup_score = cadet.avg_event(scores, pushup_score_values, event='pushups')
        avg_situp_score = cadet.avg_event(scores, situp_score_values, event='situps')
        avg_two_mile_score = cadet.avg_event(scores, two_mile_score_values, event='Two-mile run')
        
        context = {
                   'cadet':cadet,
                   'scores':ordered_scores,
                   'max_score':max_score,
                   'avg_score':avg_score,
                   'avg_pushup_score':avg_pushup_score,
                   'avg_situp_score':avg_situp_score,
                   'avg_two_mile_score':avg_two_mile_score,
                   'weakest_event':weakest_event,
                   'strongest_event':strongest_event,
                   'tab':tab,
                   }
        return render(request, self.template_name, context)

class CompanyStats(View):
    template_name = 'personnel/company_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})
    
class CompanyListing(View):
    template_name='personnel/company_listing.html'
    
    companies = Company.objects.all()
    platoons = Platoon.objects.all()
    
    def get(self, request):
        return render(request, self.template_name, {'companies': self.companies, 'platoons': self.platoons})
    
class CompanyCadetListing(View):
    template_name = 'personnel/company_cadet_listing.html'
    
    def get(self, request, company_name):
        company = Company.objects.get(name = company_name)
        cadets = Cadet.objects.filter(company = company)
        return render(request, self.template_name, {'company': company, 'cadets': cadets})

class MSlevelStats(View):
    template_name = 'personnel/ms_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})

class MSlevelListing(View):
    template_name='personnel/ms_listing.html'
    
    ms_classes = MsLevel.objects.all()
    
    def get(self, request):
        return render (request, self.template_name, {'ms_classes': self.ms_classes})
    
    
class MScadetListing(View):
    template_name = 'personnel/ms_cadet_listing.html'
    
    def get(self, request, ms_class):
        ms_class = MsLevel.objects.get(name=ms_class)
        cadets = Cadet.objects.filter(ms_level = ms_class)
        return render (request, self.template_name, {'ms_class': ms_class, 'cadets': cadets})
    
    