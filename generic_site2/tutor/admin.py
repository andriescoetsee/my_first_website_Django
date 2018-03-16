from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Event)
admin.site.register(models.EventTemplate)
admin.site.register(models.Instructor)
admin.site.register(models.Student)
admin.site.register(models.Lesson)
admin.site.register(models.LessonType)
admin.site.register(models.Parent)