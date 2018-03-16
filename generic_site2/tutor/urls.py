from django.conf.urls import url
from . import views

app_name = 'tutor'

urlpatterns = [
   url(r'^calendar/$', views.TutorCalendar.as_view(), name='calendar'),
   url(r"^export/$", views.EventExportExcel.as_view(), name="export_event"),
   url(r"^landing/$", views.TutorDashboard.as_view(), name="dashboard"),
   url(r"^list/$", views.TutorEventListView.as_view(), name="all_sessions"),
]
