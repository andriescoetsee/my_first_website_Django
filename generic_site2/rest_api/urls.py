from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tutor/$', views.TutorEventsList.as_view()),
	url(r'^bible_study/announcements/$', views.AnnouncementSerializer.as_view()),
	url(r'^bible_study/questions/$', views.QuestionSerializer.as_view()),
	url(r'^bible_study/prayer_topics/$', views.PrayerTopicSerializer.as_view()),
]