#!/usr/bin/python3.6

import os

#os.chdir("C:/Users/Andries Coetsee/myWebsite2/generic_site2/tutor/utils")
os.chdir("/home/growlearning/myWebsite/generic_site2")
os.environ['DJANGO_SETTINGS_MODULE'] = 'generic_site2.settings'

import django
django.setup()

from django.conf import settings
from tutor.models import Event, Instructor
from utils.SMS_Interface import SMS_Notification
from datetime import date, datetime, timedelta

sms = SMS_Notification()

tomorrow = date.today() + timedelta(days=1)
tomorrow_name = tomorrow.strftime('%A')

sms_msg = "Daily Tutor " + tomorrow.strftime('%Y-%m-%d') + " :-) "

if tomorrow_name == 'Sunday':
    print("Tomorrow is Sabbath day - rest")
else:
    sessions = Event.objects.filter(day_dt=tomorrow).order_by('from_time')
    if sessions.exists():
        for session in sessions :
            sms_msg += session.daily_SMS_format()
            sms_msg += ';-)'
    else :
        sms_msg += "No sessions today"

    for tutor in Instructor.objects.filter(name="Christiaan"):
        sms.push(tutor.cell_nr, sms_msg)

    result, sms_to = sms.send_bulk()

    if result == True:
        print("Instructor Daily SMS was sent successfully!")
    else :
        print("Instructor Daily SMS failed ",sms_to)


