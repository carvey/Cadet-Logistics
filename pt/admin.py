from django.contrib import admin

from pt.models import PtTest, PtScore#, Time


class PtTestAdmin(admin.ModelAdmin):
    pass
admin.site.register(PtTest, PtTestAdmin)

class PtScoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(PtScore, PtScoreAdmin)
