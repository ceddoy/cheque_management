from django.contrib import admin

from chequeapp.models import Printer, Check


class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_type', 'point',)
    list_filter = ('check_type', 'point',)


class CheckAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'printer', 'type', 'status',)
    list_filter = ('type', 'status', 'printer')


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
