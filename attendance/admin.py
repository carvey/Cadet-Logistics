from django.contrib import admin
from attendance.models import GenericEvent, ClassEvent, PtEvent, LabEvent, FtxEvent

class PtEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(PtEvent, PtEventAdmin)

class ClassEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClassEvent, ClassEventAdmin)

class GenericEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(GenericEvent, GenericEventAdmin)

class LabEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(LabEvent, LabEventAdmin)

class FtxEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(FtxEvent, FtxEventAdmin)