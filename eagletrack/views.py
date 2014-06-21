from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import View

from eagletrack.models import Cadet

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

class CompanyStats(View):
    template_name = 'eagletrack/company_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})
    
class CompanyListing(View):
    template_name='eagletrack/company_listing.html'
    def get(self, request):
        return render(request, self.template_name, {})

class MSlevelStats(View):
    template_name = 'eagletrack/ms_stats.html'
    def get(self, request):
        return render (request, self.template_name, {})

class MSlevelListing(View):
    template_name='eagletrack/ms_listing.html'
    def get(self, request):
        return render (request, self.template_name, {})