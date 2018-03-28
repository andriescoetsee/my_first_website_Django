#!/usr/bin/python3.6

import os

#os.chdir("C:/Users/Andries Coetsee/myWebsite2/generic_site2/tutor/utils")
os.chdir("/home/growlearning/myWebsite/generic_site2")
os.environ['DJANGO_SETTINGS_MODULE'] = 'generic_site2.settings'

import django
django.setup()

from django.conf import settings
from tutor.models import Event, EventTemplate
from datetime import date, datetime, timedelta
from itertools import groupby

#pip install python-dateutil
from dateutil.relativedelta import relativedelta
from calendar import monthrange


last_day_this_month = monthrange(date.today().year , date.today().month)[1]
second_last_day = last_day_this_month - 1

if second_last_day != date.today().day:
    print("Not 2nd last day quiting...")
    quit()
else :
    print("We are populating next month with template")
    print("Second last day: ",second_last_day)
    print( date.today().day)

next_month = date.today() + relativedelta(months=+1)
last_day = monthrange(next_month.year, next_month.month)[1]


# last_dt = date(next_month.year, next_month.month, last_day)
first_dt = date(next_month.year, next_month.month, 1)

eventsT = EventTemplate.objects.order_by('week_day','from_time')

field = lambda x: x.week_day.nr
eventTD = dict(
            [(day, list(items)) for day, items in groupby(eventsT, field)]
          )

for day in range(0, last_day):
     dt = first_dt + timedelta(days=day)

     if dt.weekday() in eventTD:
        for eventT in eventTD[dt.weekday()]:
            event = Event.objects.get_or_create(
                                        day_dt = dt,
                                        from_time=eventT.from_time,
                                        to_time=eventT.to_time,
                                        instructor=eventT.instructor,
                                        student=eventT.student,
                                        lesson_type=eventT.lesson_type)[0]
            print("created: ", event)

