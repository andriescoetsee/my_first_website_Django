from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, timedelta
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView, FormView, View)

from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from dateutil.relativedelta import relativedelta
from calendar import monthrange

from bible_study.forms import (
								  # ScriptureForm, 
                                  NoteForm, 
                                  QuestionForm,
#                                 BibleStudyEventForm, 
#                                 MyAnswerForm,
#                                 MyNoteForm,
#                                 PostForm,
                                  DashboardForm,
#                                 EmailBibleStudyForm
								)


from bible_study.models import (DashboardCard, 
                                Scripture, 
                                Note, 
                                Question, 
                                BibleStudyEvent, 
                                BibleStudyEventType,
                                BibleStudyUser)

from utils.models import PublicHoliday

from bible_study.utils.Word_Export import BibleStudyExportWord

class DashboardListView( LoginRequiredMixin, PermissionRequiredMixin, ListView):
    redirect_field_name = 'bible_study/dashboardcard_list.html'
    login_url = '/accounts/login/bible_study/'

    permission_required = ('accounts.bible_study_participant',)

    model = DashboardCard

    def get_queryset(self):
        dashboard = DashboardCard.objects.order_by('card_type__rank','-update_date')
        return dashboard

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['scripture_prev'] = Scripture.objects.get(status = "PREV")
        context['scripture_next'] = Scripture.objects.get(status = "NEXT")
        
        return context

class DashboardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/bible_study/'
    redirect_field_name = 'bible_study/dashboardcard_list.html'

    permission_required = ('accounts.bible_study_participant',)

    form_class = DashboardForm

    model = DashboardCard

class ScriptureListView( LoginRequiredMixin, PermissionRequiredMixin, ListView):
    redirect_field_name = 'bible_study/dashboardcard_list.html'
    login_url = '/accounts/login/bible_study/'

    permission_required = ('accounts.bible_study_participant')

    model = Scripture

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['books'] = Scripture.objects.order_by('book').values_list('book', flat=True).distinct()
        context['next_study_book'] = Scripture.objects.get(status = 'NEXT').book
        return context

class ScriptureDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    redirect_field_name = 'bible_study/dashboardcard_list.html'
    login_url = '/accounts/login/bible_study/'
    
    permission_required = ('accounts.bible_study_participant')
    model = Scripture

class NoteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/bible_study/'
    redirect_field_name = 'bible_study/dashboardcard_list.html'

    permission_required = ('accounts.bible_study_participant','accounts.is_bible_study_admin')

    form_class = NoteForm

    model = Note

class QuestionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    redirect_field_name = 'bible_study/dashboardcard_list.html'
    login_url = '/accounts/login/bible_study/'

    template_name = 'bible_study/question_detail.html'
    
    permission_required = ('accounts.bible_study_participant')
    model = Scripture

class QuestionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/bible_study/'
    redirect_field_name = 'bible_study/dashboardcard_list.html'

    permission_required = ('accounts.bible_study_participant','accounts.is_bible_study_admin')

    form_class = QuestionForm

    model = Question

class QuestionExportWord(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/accounts/login/bible_study/'
    redirect_field_name = 'bible_study/dashboardcard_list.html'

    success_url = reverse_lazy('bible_study:scripture_list')
    permission_required = ('accounts.bible_study_participant',)

    def get(self, request, *args, **kwargs):
        
        scripture =Scripture.objects.get(pk=kwargs["pk"])

        doc_name = scripture.get_title_clean()  + "_" + "Questions.docx"

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename= "%s" ' % doc_name
        
        try :
            docx_data = BibleStudyExportWord(scripture,request.user, "QUESTIONS")
            response.write(docx_data)
            return response

        except :
            messages.error(self.request, "Export to Word failed")
            return redirect('bible_study:scripture_detail', pk=scripture.pk)

class NoteExportWord(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/accounts/login/bible_study/'
    redirect_field_name = 'bible_study/dashboardcard_list.html'

    success_url = reverse_lazy('bible_study:scripture_list')
    permission_required = ('accounts.bible_study_participant',)

    def get(self, request, *args, **kwargs):
        
        scripture =Scripture.objects.get(pk=kwargs["pk"])

        doc_name = scripture.get_title_clean()  + "_" + "Notes.docx"

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename= "%s" ' % doc_name
        
        try :
            docx_data = BibleStudyExportWord(scripture,request.user, "NOTES")
            response.write(docx_data)
            return response

        except :
            messages.error(self.request, "Export to Word failed")
            return redirect('bible_study:scripture_detail', pk=scripture.pk)

class BibleStudyCalendar(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'bible_study/bible_study_calendar.html'
    login_url = '/accounts/login/bible_study/'
    redirect_field_name = 'bible_study/bible_study_calendar.html'
    
    permission_required = ('accounts.bible_study_participant')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = BibleStudyEventType.objects.all().order_by('name')

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

        events = BibleStudyEvent.objects.filter(day_dt__gte=start, day_dt__lte=end)

        event_arr = []

        
        for i in events:

            event_sub_arr = {}
            event_sub_arr['id'] = i.pk
            event_sub_arr['title'] = i.event_type.name 
            event_sub_arr['start'] = i.day_dt.strftime("%Y-%m-%d") 
            event_sub_arr['allDay'] = 'true'
            # event_sub_arr['end'] = i.get_end_date()
            event_sub_arr['event_type'] = i.event_type.name
            event_sub_arr['event_type_id'] = i.event_type.id
            event_sub_arr['scripture'] =  i.scripture
            event_sub_arr['note'] = i.note
            
            if i.event_type.name[0:3] == "SWS" :
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
                
        bds = BibleStudyUser.objects.filter( Q(birthday_month=start_month) | Q(birthday_month=middle_month) |  Q(birthday_month=end_month))

        for bd in bds:
            # get new birthday by adjusting the year
            new_bd = bdd[ bd.birthday_month ] + timedelta(days=(bd.birthday.day - 1))
            event_sub_arr = {}
            event_sub_arr['title'] = bd.user.first_name + " " + bd.user.last_name 
            event_sub_arr['allDay'] = 'true'
            event_sub_arr['start'] = new_bd.strftime("%Y-%m-%d") 
            event_sub_arr['day_type'] = 'BIRTHDAY'
            event_sub_arr['color'] = '#3c8dbc'
            event_sub_arr['textColor'] = 'white'
            event_arr.append(event_sub_arr)

        return JsonResponse(event_arr, safe=False)

    def delete_event(self, id ) :
        event = BibleStudyEvent.objects.get(pk=id)
        event.delete()
        return 'true'

    def add_event(self, request) :
    
        event_type_id = get_object_or_404(BibleStudyEventType, pk=request.POST['event_type_id'])

        event = BibleStudyEvent.objects.create(scripture=request.POST['scripture'],
                                     day_dt=request.POST['date'][0:10],
                                     note=request.POST['note'],
                                     event_type=event_type_id
                                     )
        return event.pk

    def update_event(self, request) :

        event = BibleStudyEvent.objects.get(pk=request.POST['id'])
        event.day_dt=request.POST['date'][0:10]
        event.save()
        
        return 'true'
