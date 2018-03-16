from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.PublicHoliday)
admin.site.register(models.WeekDay)
