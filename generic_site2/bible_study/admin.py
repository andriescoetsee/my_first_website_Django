from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.DashboardCard)
admin.site.register(models.DashboardCardType)

admin.site.register(models.Scripture)
admin.site.register(models.Verse)
admin.site.register(models.Note)
admin.site.register(models.BibleStudyEvent)
# admin.site.register(models.MyAnswer)
# admin.site.register(models.MyNote)
# admin.site.register(models.Post)
admin.site.register(models.BibleStudyUser)
admin.site.register(models.BibleStudyEventType)
admin.site.register(models.Question)
