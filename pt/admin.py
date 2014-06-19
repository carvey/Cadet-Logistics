from django.contrib import admin

from pt.models import PtTest, PtScore#, Time

"""
class TimeInlineAdmin(admin.TabularInline):
    model = Time
    extra = 1
    max_num = 1

class TimeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Time, TimeAdmin)
"""

class PtTestAdmin(admin.ModelAdmin):
    pass
admin.site.register(PtTest, PtTestAdmin)

class PtScoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(PtScore, PtScoreAdmin)
