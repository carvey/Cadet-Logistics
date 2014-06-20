from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from pt.models import PtTest

class Dashboard(View):
    template_name = 'pt/dashboard.html'
    pt_tests = PtTest.objects.all()
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'tests':self.pt_tests})

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