from django.contrib import admin

from mbnjattend.models import (Course, Grade, Information,
                                Profile, Roster, Schedule, Schoolyear, Transaction)
# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('transdate',)

admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(Information)
admin.site.register(Profile)
admin.site.register(Roster)
admin.site.register(Schoolyear)
admin.site.register(Schedule)
admin.site.register(Transaction, TransactionAdmin)
