from django.contrib import admin

# Register your models here.
from mbnjdash.models import (Announcement, Performance)

admin.site.register(Announcement)
admin.site.register(Performance)
