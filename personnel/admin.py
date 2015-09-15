from django.contrib import admin

from personnel.models import Cadet, Cadre, Company, Platoon
from pt.models import PtScore


class PtScoreInlineAdmin(admin.TabularInline):
    model = PtScore
    fk_name='cadet'

class CadetAdmin(admin.ModelAdmin):
    list_display=('__unicode__', 'company', 'ms_level', 'gpa')
    inlines = [
               PtScoreInlineAdmin,
               ]
admin.site.register(Cadet, CadetAdmin)

class CadreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cadre, CadreAdmin)

class CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Company, CompanyAdmin)

class PlatoonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Platoon, PlatoonAdmin)