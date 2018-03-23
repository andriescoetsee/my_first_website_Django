
from django.conf.urls import url
from . import views


app_name = 'bible_study'

urlpatterns = [
    url(r'^dashboard/$',views.DashboardListView.as_view(),name='dashboard'),
    url(r'^dashboard/(?P<pk>\d+)/edit/$',views.DashboardUpdateView.as_view(),name='update_dashboard'),    
    
    url(r'^list/$',views.ScriptureListView.as_view(),name='scripture_list'),

    url(r'^(?P<pk>\d+)/detail/$', views.ScriptureDetailView.as_view(), name='scripture_detail'),
    url(r'^note/(?P<pk>\d+)/edit/$', views.NoteUpdateView.as_view(), name='note_update'),

    url(r"^questions/(?P<pk>\d+)/export/$", views.QuestionExportWord.as_view(), name="export_questions"),
    url(r"^notes/(?P<pk>\d+)/export/$", views.NoteExportWord.as_view(), name="export_notes"),

    url(r'^question/(?P<pk>\d+)/detail/$', views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^question/(?P<pk>\d+)/edit/$', views.QuestionUpdateView.as_view(), name='question_update'),

    url(r'^calendar/$', views.BibleStudyCalendar.as_view(), name='calendar'),

    # url(r'^new/$', views.ScriptureCreateView.as_view(), name='create_scripture'),
    # url(r'^(?P<pk>\d+)/edit/$', views.ScriptureUpdateView.as_view(), name='update_scripture'),
    # url(r'^(?P<pk>\d+)/remove/$', views.ScriptureDeleteView.as_view(), name='remove_scripture'),
    # url(r'^(?P<pk>\d+)/email/$', views.EmailBibleStudyFormView.as_view(), name='email_scripture'),

    # url(r'^(?P<pk>\d+)/detail/$', views.ScriptureDetailView.as_view(), name='detail_scripture'),
    # url(r'^note/(?P<pk>\d+)/new/$', views.NoteCreateView.as_view(), name='create_note'),
    # url(r'^note/(?P<pk>\d+)/edit/$', views.NoteUpdateView.as_view(), name='update_note'),
    # url(r'^note/(?P<pk>\d+)/remove/$', views.NoteDeleteView.as_view(), name='remove_note'),

    # url(r'^answer/(?P<pk>\d+)/detail/$', views.MyAnswerDetailView.as_view(), name='detail_myanswer'),
    # url(r'^answer/(?P<pk>\d+)/new/$', views.MyAnswerCreateView.as_view(), name='create_myanswer'),
    # url(r'^answer/(?P<pk>\d+)/edit/$', views.MyAnswerUpdateView.as_view(), name='update_myanswer'),
    # url(r'^answer/(?P<pk>\d+)/remove/$', views.MyAnswerDeleteView.as_view(), name='remove_myanswer'),

    # url(r'^my_note/(?P<pk>\d+)/detail/$', views.MyNoteDetailView.as_view(), name='detail_mynote'),
    # url(r'^my_note/(?P<pk>\d+)/new/$', views.MyNoteCreateView.as_view(), name='create_mynote'),
    # url(r'^my_note/(?P<pk>\d+)/edit/$', views.MyNoteUpdateView.as_view(), name='update_mynote'),
    # url(r'^my_note/(?P<pk>\d+)/remove/$', views.MyNoteDeleteView.as_view(), name='remove_mynote'),
    
    # url(r'^event_list/$',views.EventListView.as_view(),name='list_event'),
    # url(r'^new_event/$', views.EventCreateView.as_view(), name='create_event'),
    # url(r'^(?P<pk>\d+)/edit_event/$', views.EventUpdateView.as_view(), name='update_event'),
    # url(r'^(?P<pk>\d+)/remove_event/$', views.EventDeleteView.as_view(), name='remove_event'),
   
    # url(r'^post/list/$',views.PostListView.as_view(),name='list_post'),
    # url(r'^post/(?P<pk>\d+)/new/$', views.PostCreateView.as_view(), name='create_post'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='update_post'),
    # url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='remove_post'),
 
    # url(r'^dashboard/list/$',views.DashboardListView.as_view(),name='list_dashboard'),
    # url(r'^dashboard/(?P<pk>\d+)/edit/$',views.DashboardUpdateView.as_view(),name='update_dashboard'),    
 
    # url(r"^questions/(?P<pk>\d+)/export/$", views.QuestionExportWord.as_view(), name="export_question"),
    # url(r"^reflection/(?P<pk>\d+)/export/$", views.ReflectionExportWord.as_view(), name="export_reflection"),
 ]