# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.urls import reverse
from utils.models import WeekDay

class EventTemplate(models.Model):
    week_day = models.ForeignKey('utils.WeekDay', related_name='week_dayT',on_delete=models.CASCADE)
    from_time = models.CharField(max_length=5)
    to_time = models.CharField(max_length=5)
    instructor = models.ForeignKey('Instructor', related_name='instructorT',on_delete=models.CASCADE)
    student = models.ForeignKey('Student', related_name='studentT',on_delete=models.CASCADE)
    lesson_type = models.ForeignKey('LessonType', related_name='lesson_typeT',on_delete=models.CASCADE)
    
    class Meta:
        ordering   = ['week_day','-from_time']

    def __str__(self):
        return  self.week_day.__str__() + "-" + self.from_time[0:5] + " - " + self.student.name + " " + self.student.surname

class Event(models.Model):
    day_dt = models.DateField()
    from_time = models.CharField(max_length=5)
    to_time = models.CharField(max_length=5)
    note = models.TextField(max_length=50,blank=True, null=True)
    lesson_comment = models.TextField(max_length=250, blank=True, null=True)
    instructor = models.ForeignKey('Instructor', related_name='instructor',on_delete=models.CASCADE)
    student = models.ForeignKey('Student', related_name='student',on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', related_name='lesson',on_delete=models.CASCADE,blank=True, null=True)
    lesson_type = models.ForeignKey('LessonType', related_name='lesson_type',on_delete=models.CASCADE)

    class Meta:
        ordering   = ['-day_dt','-from_time']

    def get_start_time(self):
        return self.from_time + ":00"
        
    def get_end_time(self):
        return self.to_time + ":00"

    def get_start_date(self):
        start_str_dt = self.day_dt.strftime("%Y-%m-%d") + " " + self.from_time + ":00"
        return datetime.strptime(start_str_dt, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        
    def get_end_date(self):
        end_str_dt = self.day_dt.strftime("%Y-%m-%d") + " " + self.to_time + ":00"
        return datetime.strptime(end_str_dt, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    def get_duration_hr(self):
        start_tm =  datetime.strptime(self.from_time[0:5],"%H:%M")
        end_tm =  datetime.strptime(self.to_time[0:5],"%H:%M")
        diff = (end_tm - start_tm)
        return diff.seconds/60/60 

    def daily_SMS_format(self):
        return self.from_time[0:5] + "-" + self.to_time[0:5] + " " + self.instructor.name

    def sms_default_msg(self):
        return str("Tutoring :-)" + self.day_dt.strftime('%Y-%m-%d') + " " + self.from_time[0:5] + "-" + self.to_time[0:5] +  " -> " + self.instructor.name + " -> " + self.student.name + " " + self.student.surname + "(" + self.lesson_type.name + ")")

    def get_absolute_url(self):
        return reverse("tutor:list")

    def get_edit_url(self):
        return reverse("tutor:update_event",kwargs={'pk':self.pk})

    def display(self):
        return self.student.name + " " + self.student.surname + " ( " + self.lesson_type.name + " )"

    def tooltip(self):
        return self.from_time[0:5] +  " - " + self.to_time[0:5] + " " + self.instructor.name + " " + self.lesson_type.name
                
    def __str__(self):
        return  self.day_dt.strftime('%Y-%m-%d') + " - " + self.student.name + " " + self.student.surname

    def get_date(self):
        return  self.day_dt.strftime('%Y-%m-%d')

    def get_from_to_time(self):
        return  self.from_time[0:5] +  " - " + self.to_time[0:5]

    def get_date_type(self):
        if (self.day_dt.strftime('%Y-%m-%d')  == (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')):
            return "TOMORROW"
        elif (self.day_dt.strftime('%Y-%m-%d')  == date.today().strftime('%Y-%m-%d')):
            return "TODAY"
        else :
            return "UNKNOWN"
        
class LessonType(models.Model):
     name = models.TextField(max_length=50)
     description = models.TextField(max_length=50, blank=True, null=True)

     def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.TextField(max_length=50)
    grade = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(max_length=50, blank=True, null=True)
    expected_outcome = models.TextField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("tutor:list")

    def __str__(self):
        return self.title + " grade %s" % self.grade

class TutorUser(models.Model):
    name = models.TextField(max_length=50)
    surname = models.TextField(max_length=50)
    e_mail = models.EmailField(blank=True, null=True)
    cell_nr = models.TextField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['name']
        unique_together = ('name', 'surname',)

    def get_absolute_url(self):
        return reverse("tutor:list")

    def __str__(self):
        return self.name + " " + self.surname

class Parent(TutorUser):
    pass
    
class Student(TutorUser):
    birthday = models.DateField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey('Parent', related_name='children',  on_delete=models.CASCADE, blank=True, null=True )   
    birthday_month = models.PositiveSmallIntegerField(blank=True, null=True)

class Instructor(TutorUser):
    pass