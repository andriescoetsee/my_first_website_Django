import urllib.request as ur
import urllib.parse
from urllib.error import URLError

from django.conf import settings
from django import forms
from django.contrib import messages

class SMS_Notification():

    msg_queue = []

    def push(self, to, msg):
        self.msg_queue.append((to, msg))

    def send_bulk(self):
    # to is a list of numbers to SMS
    # return list of numbers as string and True or False
            
        for sms in self.msg_queue:
            sms_to = sms[0]
            # sms_to =  ','.join([str(i) for i in sms[0]])

            data = { 'Type' : 'sendparam',
                'username' : settings.SMS_GATEWAY_UN,
                'password' : settings.SMS_GATEWAY_PW,
                'data1' : sms[1], # this is the string to SMS
                'numto' : sms_to
            }

            print(sms[1])

            url_values = urllib.parse.urlencode(data)
            url = settings.SMS_GATEWAY_URL
            full_url = url + '?' + url_values

            try :
                s = ur.urlopen(full_url)
                #sl = s.read() #this is the HTML return output
                #print(s)
            except :
                print("failed")
                return False, sms_to

        return True, ""

    def send(self, to, msg):
    # to is a list of numbers to SMS
    # return list of numbers as string and True or False
        
        sms_to =  ','.join([str(i) for i in to])

        data = { 'Type' : 'sendparam',
            'username' : settings.SMS_GATEWAY_UN,
            'password' : settings.SMS_GATEWAY_PW,
            'data1' : msg,
            'numto' : sms_to
            }

        print(msg)
        
        url_values = urllib.parse.urlencode(data)
        url = settings.SMS_GATEWAY_URL
        full_url = url + '?' + url_values

        try :
            #print(full_url)
            s = ur.urlopen(full_url)

        except :
            sl = s.read() #this is the HTML return output
            print(sl)
            return False, sms_to

        return True, "" 
