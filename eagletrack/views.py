from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import View

from eagletrack.models import Cadet, Company, MsLevel, Platoon

# Create your views here.

class index(View):
    template_name = "index.html"
    def get(self, request):
        return render(request, self.template_name, {})
    
    
class CPview(View):
    template_name = "eagletrack/control_panel.html"
    def get(self, request):
        return render (request, self.template_name, {})

class Dashboard(View):
    template_name = "eagletrack/dashboard.html"
    def get(self, request):
        return render (request, self.template_name, {})
    
class CadetStats(View):
    template_name = 'eagletrack/cadet_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})

class CadetListing(View):
    template_name='eagletrack/cadet_listing.html'
    
    cadets = Cadet.objects.all()
    
    def get(self, request):
        return render (request, self.template_name, {'cadets': self.cadets})
    
class CadetPage(View):
    template_name='eagletrack/cadet_page.html'
    
    def get(self, request, eagle_id):
        cadet = Cadet.objects.get(eagle_id = eagle_id)
        return render(request, self.template_name, {'cadet': cadet})

class CompanyStats(View):
    template_name = 'eagletrack/company_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})
    
class CompanyListing(View):
    template_name='eagletrack/company_listing.html'
    
    companies = Company.objects.all()
    platoons = Platoon.objects.all()
    
    def get(self, request):
        return render(request, self.template_name, {'companies': self.companies, 'platoons': self.platoons})
    
class CompanyCadetListing(View):
    template_name = 'eagletrack/company_cadet_listing.html'
    
    def get(self, request, company_name):
        company = Company.objects.get(name = company_name)
        cadets = Cadet.objects.filter(company = company)
        return render(request, self.template_name, {'company': company, 'cadets': cadets})

class MSlevelStats(View):
    template_name = 'eagletrack/ms_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})

class MSlevelListing(View):
    template_name='eagletrack/ms_listing.html'
    
    ms_classes = MsLevel.objects.all()
    
    def get(self, request):
        return render (request, self.template_name, {'ms_classes': self.ms_classes})
    
    
class MScadetListing(View):
    template_name = 'eagletrack/ms_cadet_listing.html'
    
    def get(self, request, ms_class):
        ms_class = MsLevel.objects.get(name=ms_class)
        cadets = Cadet.objects.filter(ms_level = ms_class)
        return render (request, self.template_name, {'ms_class': ms_class, 'cadets': cadets})
    
    