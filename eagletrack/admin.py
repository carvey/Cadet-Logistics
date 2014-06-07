from django.contrib import admin

from django.contrib import admin

from eagletrack.models import Cadet, Cadre


class CadetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cadet, CadetAdmin)

class CadreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cadre, CadreAdmin)