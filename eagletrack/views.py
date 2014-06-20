from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import View

# Create your views here.

class index(View):
    template_name = "sbadmin/index.html"
    def get(self, request):
        return render(request, self.template_name, {})
    
class CPview(View):
    
    def get(self, request):
        return HttpResponse("CPview")

class Dashboard(View):
    
    def get(self, request):
        return HttpResponse("Dashboard")

class CadetListing(View):
    
    def get(self, request):
        return HttpResponse("Cadet Listing")

class CadetStats(View):
    
    def get(self, request):
        return HttpResponse("Cadet stats")

class CompanyStats(View):
    
    def get(self, request):
        return HttpResponse("Company Stats")

class MSlevelStats(View):
    
    def get(self, request):
        return HttpResponse("MSlevel stats")
    