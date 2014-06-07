from django.contrib import admin

from eagletrack.models import Cadet, Cadre, Company, Platoon


class CadetAdmin(admin.ModelAdmin):
    pass
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