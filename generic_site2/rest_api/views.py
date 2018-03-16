from django.shortcuts import render
from rest_framework import generics
from tutor.serializers import TutorEventsSerializer
# from bible_study.serializers import AnnouncementSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime, timedelta
from django.db.models import Q

from tutor.models import Event
# from bible_study.models import DashboardCard, Question, Scripture

class TutorEventsList(generics.ListAPIView):
    serializer_class = TutorEventsSerializer

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Event.objects.filter(Q (date_dt=date.today()) | Q (date_dt=(date.today() + timedelta(days=1)))).order_by('-date_and_time', '-from_time')

# class AnnouncementSerializer(generics.ListAPIView):
#     queryset = DashboardCard.objects.filter(card_type__name="ANNOUNCEMENTS")
#     serializer_class = AnnouncementSerializer

#     permission_classes = (IsAuthenticated, )

# class QuestionSerializer(generics.ListAPIView):
#     queryset = Scripture.objects.filter(status="NEXT")
#     serializer_class = QuestionSerializer

#     permission_classes = (IsAuthenticated, )
