from django.db import models

# from accounts.models import User

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.urls import reverse
from django.contrib import messages

# from accounts.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class DashboardCardType(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=100, blank=True, null=True, default="")
    rank = models.PositiveSmallIntegerField(default=-1)

    class Meta:
        ordering : ['name']

    def get_absolute_url(self):
        return reverse("bible_study:dashboard")

    def __str__(self):
        return self.name

class DashboardCard(models.Model):
    update_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='cards', on_delete=models.CASCADE )
    card_type = models.ForeignKey('DashboardCardType', related_name='cards', on_delete=models.CASCADE )
    
    #header = models.TextField(max_length=50, blank=True, null=True, default="")
    image = models.TextField(max_length=50, blank=True, null=True, default="")
    title = models.TextField(max_length=100, blank=True, null=True)
    text  = models.TextField(max_length=250, blank=True, null=True)
    list_item1 = models.TextField(max_length=100, blank=True, null=True, default="")
    list_item2 = models.TextField(max_length=100, blank=True, null=True, default="")
    list_item3 = models.TextField(max_length=100, blank=True, null=True, default="")
    link = models.TextField(max_length=100, blank=True, null=True, default="")

    class Meta:
        ordering : ['card_type','update_date', 'user']

    def get_api_announcement_text(self):
        return self.title + " " + self.text

    def get_absolute_url(self):
        return reverse("bible_study:dashboard")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.update_date = datetime.today()
        super(DashboardCard, self).save(*args, **kwargs)

class BibleStudyUser(models.Model):
    user = models.OneToOneField(User, related_name='bible_study_user', on_delete=models.CASCADE )
    cell_nr = models.TextField(max_length=50, blank=True, null=True)
    birthday = models.DateField(max_length=50, blank=True, null=True)
    birthday_month = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_birthday(self):
        if self.birthday:
            day = self.birthday.day
            mth = self.birthday.month
            year = datetime.datetime.now().year 
            return date(year, mth, day)
        else :
            return self.birthday

    class Meta:
        ordering : ['user']

    def get_absolute_url(self):
        return reverse("bible_study:dashboard")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Scripture(models.Model):

    STUDY_STATES = (
    ('OPEN','Open'),
    ('STUDIED', 'Studied'),
    ('NEXT','Next'),
    ('PREV', 'Previous'),
    )

    book = models.TextField(max_length=50)
    passage = models.TextField(max_length=50)
    title = models.TextField(max_length=50)
    key_verse = models.TextField(max_length=20,)
    main_point = models.TextField(max_length=2000, blank=True, null=True)
    summary = models.TextField(max_length=2000, blank=True, null=True)
    verses_linked = models.BooleanField(default=False)
    notes_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STUDY_STATES, default='OPEN')

    class Meta:
        ordering   = ['-book', '-pk']

    def get_title_clean(self):
        # removes commas replacing it with _
        return self.title.replace(",","_")


    def get_chapter(self):
        return int(self.passage.split(":")[0])

    def get_absolute_url(self):
        return reverse("bible_study:dashboard")

    def __str__(self):
        return self.book + " " + self.passage + ":" + self.title  

    def get_passage_api(self):
        return self.book + " " + self.passage
    
    def get_key_verse_text(self):

        kv = self.key_verse.split(":")

        vs = Verse.objects.get(book = self.book, chapter = kv[0], verse_nr = kv[1] )

        return vs.verse_text

    def get_latest_post(self):
        try:
            max_post = Post.objects.filter(scripture=self).latest('create_date')
            return max_post.create_date.strftime('%b-%d') + " by " + max_post.user.username
        except :
            return ""

    def has_post_last_week (self):
        try :
            week_ago = date.today() - timedelta(days=7)
            max_post = Post.objects.filter(scripture=self,create_date__gte=week_ago).latest('create_date')
            return True
        except :
            return False

    def save(self, *args, **kwargs):
        super(Scripture, self).save(*args, **kwargs)

        if not self.verses_linked:
            # Generate Verses for the passage
            # we expect this format "1:1- 5;1:7- 10" 
            # per passage and ';'' for more than 1 passage (could be different chapter)

            # remove white spaces
            clean_passage = [x.replace(' ', '') for x in self.passage]
            self.passage = ''.join(clean_passage )

            #make a list of passages
            passages = self.passage.split(";")

            #Key verse
            # remove white spaces
            clean_kv = [x.replace(' ', '') for x in self.key_verse]
            self.key_verse = ''.join(clean_kv )

            #get kv chapter and verse
            kv = self.key_verse.split(":")

            vs = Verse.objects.get(book = self.book, chapter = kv[0], verse_nr = kv[1] )
            
            # note = Note(seq_nr = 1,  scripture = self, verse_heading = 'Key Verse', verse = vs )
            # note.save()

            #heading
            note = Note(seq_nr = 5,  scripture = self, verse_heading = 'Overview of passage')
            note.save()

            for i, item in enumerate(passages):
                chapter = passages[i].split(":")[0]
                verses = passages[i].split(":")[1]
                from_verse = verses.split("-")[0]
                to_verse = verses.split("-")[1]
                
                for i in range(int(from_verse), int(to_verse)+1 ):
                    # get the relevant verse 
                    vs = Verse.objects.get(book = self.book, chapter = chapter, verse_nr = i)
                    note = Note(seq_nr = i*10,  scripture = self, verse = vs )
                    note.save() 

            seq_nr = (i * 10) + 50
            note = Note(seq_nr = seq_nr,  scripture = self, verse_heading = 'Conclusion')
            note.save()

            seq_nr +=50; 
            note = Note(seq_nr = seq_nr,  scripture = self, verse_heading = 'Application')
            note.save()

            self.verses_linked = True

            self.save()

class Note(models.Model):
    seq_nr = models.SmallIntegerField(default=-1)
    note = models.TextField(max_length=3000, blank=True, null=True)
    scripture = models.ForeignKey('Scripture', related_name='notes',on_delete=models.CASCADE)
    verse = models.ForeignKey('Verse', related_name='verses',blank=True, null=True, on_delete=models.SET_NULL )
    verse_heading = models.TextField(max_length=150, blank=True, null=True)

    
    class Meta:
        ordering   = ['scripture','seq_nr']

    def get_absolute_url(self):
        return reverse("bible_study:scripture_detail",kwargs={'pk':self.scripture.pk})

    def __str__(self):
        if self.verse and not self.verse_heading:
            return self.scripture.title + " : " + str(self.verse.chapter) +  ":" + str(self.verse.verse_nr)
        elif self.verse_heading:
            return self.scripture.title + " : " + self.verse_heading
        else :
            return self.scripture.title 
            
class Verse(models.Model):
    book  = models.TextField(max_length=50) 
    chapter  = models.PositiveSmallIntegerField()
    verse_nr = models.PositiveSmallIntegerField()
    verse_text = models.TextField(max_length=1000 )

    class Meta:
        ordering   = ['book','chapter','verse_nr']
        unique_together = ('book','chapter','verse_nr')

    def get_absolute_url(self):
        return reverse("bible_study:list_scripture")

    def __str__(self):
        return self.verse_text

class Question(models.Model):
    from_verse = models.SmallIntegerField(default=-1)
    to_verse = models.SmallIntegerField(default=-1)
    question =  models.TextField(max_length=1000, blank=True, null=True)
    scripture = models.ForeignKey('Scripture', related_name='questions',on_delete=models.CASCADE)
       
    class Meta:
        ordering   = ['scripture','from_verse']

    def get_verses(self):
        return Verse.objects.filter(book=self.scripture.book,
                                    chapter= self.scripture.get_chapter(),
                                    verse_nr__gte = self.from_verse,
                                    verse_nr__lte = self.to_verse)

    def get_absolute_url(self):
        return reverse("bible_study:list_scripture")

    def __str__(self):
        return self.scripture.__str__() + " :" + str(self.from_verse) + " - " + str(self.to_verse)

class MyAnswer(models.Model):
    user = models.ForeignKey(User, related_name='question_answers', on_delete=models.CASCADE )
    answer = models.TextField(max_length=2000, blank=True, null=True, default="")
    question = models.ForeignKey('Question', related_name='my_answer',on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'question',)
        ordering   = ['user','question']

    def get_absolute_url(self):
        return reverse("bible_study:detail_myanswer",kwargs={'pk':self.question.scripture.pk})

    def __str__(self):
        return self.user.username + " answer on " + self.question.__str__() 

class MyNote(models.Model):
    user = models.ForeignKey(User, related_name='note',on_delete=models.CASCADE )
    note = models.TextField(max_length=2000, blank=True, null=True, default="")
    scripture = models.ForeignKey('Scripture', related_name='my_note',on_delete=models.CASCADE)
    
    class Meta:
        ordering   = ['user','scripture']

    def get_absolute_url(self):
        return reverse("bible_study:detail_mynote",kwargs={'pk':self.scripture.pk})

    def __str__(self):
        return self.scripture.title

class Post(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE )
    comment = models.TextField(max_length=2000, blank=True, null=True, default="")
    scripture = models.ForeignKey('Scripture', related_name='posts',on_delete=models.CASCADE)
    
    class Meta:
        ordering : ['create_date']

    def get_absolute_url(self):
        return reverse("bible_study:list_scripture")

    def __str__(self):
        return self.scripture.title

class BibleStudyEventType(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name

class BibleStudyEvent(models.Model):
    day_dt = models.DateField()
    note = models.TextField(max_length=50,blank=True, null=True)
    scripture = models.TextField(max_length=50,blank=True, null=True)
    event_type = models.ForeignKey('BibleStudyEventType', related_name='events',on_delete=models.CASCADE)
    
    class Meta:
        ordering   = ['-day_dt']

    def get_absolute_url(self):
        # return reverse("bible_study:list_event")
        return reverse("bible_study:dashboard")

    def display(self):

        display_txt = self.event_type.name + " "

        if self.scripture :
            display_txt += self.scripture
        
        return display_txt

    def tooltip(self):
        return self.note

    def __str__(self):
        return self.day_dt.strftime('%Y-%m-%d') + " - " + self.event_type.name

