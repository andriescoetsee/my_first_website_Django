from django.contrib import admin

# Register your models here.
from . import models

class EventTemplateAdmin(admin.ModelAdmin) :
    list_filter = ['instructor','week_day','lesson_type','student',]
    list_display = ['week_day','from_time', 'to_time','instructor','student','lesson_type' ]


class EventAdmin(admin.ModelAdmin) :
    list_filter = ['instructor','lesson_type','student',]
    list_display = ['day_dt','from_time', 'to_time','instructor','student','lesson_type' ]

class EventAdmin(admin.ModelAdmin) :
    list_filter = ['instructor','lesson_type','student',]
    list_display = ['day_dt','from_time', 'to_time','instructor','student','lesson_type' ]

class StudentAdmin(admin.ModelAdmin) :
    list_filter = ['name','surname',]
    list_display = ['name','surname', 'birthday','birthday_month','cell_nr', 'e_mail']
    
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.EventTemplate, EventTemplateAdmin)
admin.site.register(models.Instructor)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Lesson)
admin.site.register(models.LessonType)
admin.site.register(models.Parent)