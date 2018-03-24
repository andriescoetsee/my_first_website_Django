from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from tutor.models import Student, Instructor, LessonType, Event
from utils.models import PublicHoliday
from datetime import date, timedelta
from django.db.models import Q
from django.urls import reverse_lazy
from tutor.utils.Export_Excel import TutorExportExcel
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from django.contrib import messages

# Create your views here.

class TutorEventListView( LoginRequiredMixin, PermissionRequiredMixin, ListView):
    redirect_field_name = 'tutor/event_list.html'
    login_url = '/accounts/login/tutor/'
    
    permission_required = ('accounts.tutor_participant')

    model = Event

class TutorDashboard(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'tutor/tutor_dashboard.html'
    login_url = '/accounts/login/tutor/'
    redirect_field_name = 'tutor/tutor_dashboard.html'
    
    permission_required = ('accounts.tutor_participant','accounts.is_tutor_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        prev_month = date.today() + relativedelta(months=-1)
        this_month_end = date(today.year, today.month, monthrange(today.year, today.month)[1])
        this_month_start = date(today.year, today.month, 1)
        prev_month_end = date(prev_month.year, prev_month.month, monthrange(prev_month.year, prev_month.month)[1])
        prev_month_start = date(prev_month.year, prev_month.month, 1)

        
        total_sessions_this_month = Event.objects.filter(day_dt__gte=this_month_start, day_dt__lte=this_month_end).count()
        total_sessions_last_month = Event.objects.filter(day_dt__gte=prev_month_start, day_dt__lte=prev_month_end).count()

        sessions = Event.objects.filter(day_dt=today)

        instructor_christiaan = get_object_or_404(Instructor, name='Christiaan') 
        instructor_sarah = get_object_or_404(Instructor, name='Sarah')  

        # get total sessions for today
        context['total_sessions_today'] = sessions.count()
        context['christiaan_total'] = sessions.filter(instructor=instructor_christiaan).count()
        context['sarah_total'] = sessions.filter(instructor=instructor_sarah).count()
        context['christiaan_sessions'] = sessions.filter(instructor=instructor_christiaan)
        context['sarah_sessions'] = sessions.filter(instructor=instructor_sarah)
        
        context['total_sessions_this_month'] = total_sessions_this_month
        context['total_sessions_last_month'] = total_sessions_last_month

        return context


class TutorCalendar(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'tutor/tutor_calendar.html'
    login_url = '/accounts/login/tutor/'
    redirect_field_name = 'tutor/tutor_calendar.html'
    
    permission_required = ('accounts.tutor_participant','accounts.is_tutor_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all().order_by('name')
        context['instructors'] = Instructor.objects.all().order_by('name')
        context['lesson_types'] = LessonType.objects.all().order_by('name')

        return context

    def get(self, request, *args, **kwargs):
    
        if request.is_ajax():
            start_dt = request.GET['start'][0:10]
            end_dt = request.GET['end'][0:10]
            return self.get_monthly_events(start_dt, end_dt)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        if request.POST['action'] == 'DELETE':
            result = 'true'
            result = self.delete_event(request.POST['id'])
            return JsonResponse({'success': result}, safe=False) 

        if request.POST['action'] == 'ADD':
            pk = self.add_event(request) 
            if pk :
                return JsonResponse({'success': 'true', 'event_id' : pk }, safe=False)
            else:
                return JsonResponse({'success': 'false'}, safe=False)

        if request.POST['action'] == 'UPDATE':
            result = self.update_event(request) 
            return JsonResponse({'success': result }, safe=False)

        return super().post(request, *args, **kwargs)

    def get_monthly_events(self, start, end):

        events = Event.objects.filter(day_dt__gte=start, day_dt__lte=end)

        event_arr = []

        for i in events:
            event_sub_arr = {}
            event_sub_arr['id'] = i.pk
            event_sub_arr['title'] = i.student.name   
            event_sub_arr['student_id'] = i.student.id 
            event_sub_arr['start'] = i.get_start_date()
            event_sub_arr['end'] = i.get_end_date()
            event_sub_arr['start_tm'] = i.get_start_time()
            event_sub_arr['end_tm'] = i.get_end_time()
            event_sub_arr['instructor_id'] = i.instructor.id
            event_sub_arr['session_type_id'] = i.lesson_type.id
            event_sub_arr['instructor'] = i.instructor.name
            event_sub_arr['session_type'] = i.lesson_type.name

            if i.instructor.name == "Christiaan":
                event_sub_arr['backgroundColor'] = 'white'
                event_sub_arr['borderColor'] = 'white'
                event_sub_arr['textColor'] = '#00a65a'
            else :
                event_sub_arr['backgroundColor'] = 'white'
                event_sub_arr['borderColor'] = 'white'
                event_sub_arr['textColor'] = '#f39c12'

            event_arr.append(event_sub_arr)

        # get public holidays for this period
        phs = PublicHoliday.objects.filter(date__gte=start, date__lte=end)

        for ph in phs:
            event_sub_arr = {}
            event_sub_arr['title'] = ph.name   
            event_sub_arr['allDay'] = 'true'
            event_sub_arr['start'] = ph.date.strftime("%Y-%m-%d") 
            event_sub_arr['day_type'] = 'HOLIDAY'
            event_sub_arr['color'] = '#f56954'
            event_sub_arr['textColor'] = 'white'

            event_arr.append(event_sub_arr)

        # birthday
        start_month = int(start[5:7])
        start_year = int(start[0:4])
        end_month = int(end[5:7])
        end_year = int(end[0:4])

        #determine middle month and year for monthly browsing
        if start_month == 12 :
            middle_month = 1
            middle_year = end_year
        else :
            middle_month = start_month + 1
            middle_year = start_year

        # this is for weekly and daily browsing
        if start_month == end_month:
            middle_month = start_month
            middle_year = start_year

        # print("start_month ", start_month)
        # print("middle_month ", middle_month)
        # print("end_month ", end_month)

        bdd = {}
        bdd[start_month] = date(start_year, start_month,1)
        bdd[middle_month] = date(middle_year, middle_month,1)
        bdd[end_month] = date(end_year, end_month,1)
                
        bds = Student.objects.filter( Q(birthday_month=start_month) | Q(birthday_month=middle_month) |  Q(birthday_month=end_month))

        for bd in bds:
            # get new birthday by adjusting the year
            new_bd = bdd[ bd.birthday_month ] + timedelta(days=(bd.birthday.day - 1))
            event_sub_arr = {}
            event_sub_arr['title'] = bd.name + " " + bd.surname  
            event_sub_arr['allDay'] = 'true'
            event_sub_arr['start'] = new_bd.strftime("%Y-%m-%d") 
            event_sub_arr['day_type'] = 'BIRTHDAY'
            event_sub_arr['color'] = '#3c8dbc'
            event_sub_arr['textColor'] = 'white'
            event_arr.append(event_sub_arr)

        return JsonResponse(event_arr, safe=False)

    def delete_event(self, id ) :
        event = Event.objects.get(pk=id)
        event.delete()
        return 'true'

    def add_event(self, request) :
    
        student = get_object_or_404(Student, pk=request.POST['student_id'])
        instructor = get_object_or_404(Instructor, pk=request.POST['instructor_id'])
        lesson_type = get_object_or_404(LessonType, pk=request.POST['session_type_id'])

        event = Event.objects.create(student=student,
                                     day_dt=request.POST['date'][0:10],
                                     from_time=request.POST['start_tm'][0:5],
                                     to_time=request.POST['end_tm'][0:5],
                                     instructor=instructor,
                                     lesson_type=lesson_type
                                     )
        return event.pk

    def update_event(self, request) :

        event = Event.objects.get(pk=request.POST['id'])
        event.day_dt=request.POST['date'][0:10]
        from_time=request.POST['start_tm'][0:5]
        to_time=request.POST['end_tm'][0:5]
        event.save()
        
        return 'true'

class EventExportExcel(LoginRequiredMixin,PermissionRequiredMixin, View):
    success_url = reverse_lazy('tutor:calendar')
    login_url = '/accounts/login/tutor/'
    
    permission_required = ('accounts.tutor_participant','accounts.is_tutor_admin')

    def get(self, request, *args, **kwargs):
        
        if request.is_ajax():
            return JsonResponse({'success': 'true'}, safe=False)
        else :
            pass

        start_dt = request.GET['start'][0:10]
        end_dt = request.GET['end'][0:10]
            
        year=int(start_dt[0:4])
        month=int(start_dt[5:7])

        named_month = date(1900, int(month), 1).strftime("%B")

        workbook_name = str(year) + "_" + named_month + "_" + "Tutor_Export.xlsx"

        response = HttpResponse(content_type="content_type='application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename= %s ' % workbook_name

        try :
            xlsx_data = TutorExportExcel(year,month)
            response.write(xlsx_data)
            return response
        except :
            messages.error(self.request, "Export to Excel failed")
            return redirect('tutor:calendar')


        