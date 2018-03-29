from django.contrib import admin

from bible_study.forms import (
								  ScriptureForm, 
                                  NoteForm, 
                                  QuestionForm,
#                                 MyAnswerForm,
#                                 MyNoteForm,
#                                 PostForm,
                                  DashboardForm,
#                                 EmailBibleStudyForm
								)

# Register your models here.
from . import models

class ScriptureAdmin(admin.ModelAdmin) :
    form = ScriptureForm
    add_form = ScriptureForm
    # search_fields = ['book','passage','status']
    list_filter = ['book','status']
    list_display = ['title','status', 'book','passage','key_verse', ]

class NoteAdmin(admin.ModelAdmin) :
    # form = NoteForm
    # add_form = NoteForm
    # search_fields = ['scripture',]
    list_filter = ['scripture',]
    list_display = ['scripture','verse_heading', 'seq_nr']


class QuestionAdmin(admin.ModelAdmin) :
    # form = QuestionForm
    # add_form = QuestionForm
    # search_fields = ['scripture',]
    list_filter = ['scripture',]
    list_display = ['scripture','from_verse', 'to_verse']

class BibleStudyEventAdmin(admin.ModelAdmin) :
    # search_fields = ['event_type',]
    list_filter = ['event_type',]
    list_display = ['day_dt','note', 'scripture','event_type']

class DashboardCardAdmin(admin.ModelAdmin) :
    # search_fields = ['card_type','user']
    list_filter = ['card_type','user']
    list_display = ['card_type','user', 'title']


admin.site.register(models.DashboardCard, DashboardCardAdmin)
admin.site.register(models.DashboardCardType)

admin.site.register(models.Scripture, ScriptureAdmin)
admin.site.register(models.Verse)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.BibleStudyEvent, BibleStudyEventAdmin)
# admin.site.register(models.MyAnswer)
# admin.site.register(models.MyNote)
# admin.site.register(models.Post)
admin.site.register(models.BibleStudyUser)
admin.site.register(models.BibleStudyEventType)
admin.site.register(models.Question, QuestionAdmin)

