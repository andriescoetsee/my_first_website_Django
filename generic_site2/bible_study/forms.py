from django import forms

from django.shortcuts import get_object_or_404

from bible_study.models import (
                                # Scripture,
                                Verse,
                                Note, 
                                # BibleStudyEvent, 
                                # MyAnswer,
                                # MyNote,
                                # Post,
                                DashboardCard,
                                # BibleStudyEventType,
                                # BibleStudyUser
                                Question
                                )

from django.contrib.auth import get_user_model
User = get_user_model()

class DashboardForm(forms.ModelForm):

    text = forms.CharField(required=True, label="Description", widget=forms.Textarea(attrs={
                                            'rows': 2, 
                                            'cols': 40,
                                            'class': "form-control"
                                            }))

    list_item1 = forms.CharField(required=False, label="Prayer Topic 1", widget=forms.Textarea(attrs={
                                            'rows': 2, 
                                            'cols': 40,
                                            'class': "form-control",
                                            'placeholder' : 'Prayer Topic'
                                            }))

    list_item2 = forms.CharField(required=False, label="Prayer Topic 2", widget=forms.Textarea(attrs={
                                            'rows': 2, 
                                            'cols': 40,
                                            'class': "form-control",
                                            'placeholder' : 'Prayer Topic'
                                            }))

    list_item3 = forms.CharField(required=False, label="Prayer Topic 3", widget=forms.Textarea(attrs={
                                            'rows': 2, 
                                            'cols': 40,
                                            'class': "form-control",
                                            'placeholder' : 'Prayer Topic'
                                            }))

    class Meta:
        fields = ['text','list_item1','list_item2','list_item3']
        model = DashboardCard

class NoteForm(forms.ModelForm):

    verse_heading = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    note = forms.CharField(required=False, 
                    widget=forms.Textarea(attrs={'rows': 75, 
                                                 'cols': 40,
                                                 # 'data-html' : 'true'
                                                # 'style' : "width: 100%; height: 200px; font-size: 14px; line-height: 18px; border: 1px solid #dddddd; padding: 10px;"
                                                 }))
    
    class Meta:
        fields = ("seq_nr", "verse_heading","verse","note")
        model = Note
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields["seq_nr"].widget.attrs['readonly'] = True
        # for foreign key need to disable like this otherwise can disable like above
        # self.fields['scripture'].required = False
        # self.fields['scripture'].widget.attrs['disabled'] = 'disabled'
        self.fields['verse'].required = False
        self.fields['verse'].widget.attrs['disabled'] = 'disabled'
        # self.fields["verse"].queryset =  Verse.objects.all()

    def clean_scripture(self):

        instance = getattr(self, 'instance', None)
        if instance:
            return instance.scripture
        else:
            return self.cleaned_data.get('scripture', None)

    def clean_verse(self):

        instance = getattr(self, 'instance', None)
        if instance:
            return instance.verse
        else:
            return self.cleaned_data.get('verse', None)

class QuestionForm(forms.ModelForm):



    from_verse = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type':'number'}))
    to_verse = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type':'number'}))
    
    question = forms.CharField(required=False, 
                    widget=forms.Textarea(attrs={'rows': 10, 
                                                 'cols': 40,
                                                #  'data-html' : 'true'
                                                # # 'style' : "width: 100%; height: 200px; font-size: 14px; line-height: 18px; border: 1px solid #dddddd; padding: 10px;"
                                                 }))
    
    class Meta:
        fields = ("from_verse", "to_verse","question",)
        model = Note
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

