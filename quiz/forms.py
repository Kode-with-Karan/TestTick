# quiz/forms.py
from django import forms
from .models import UploadedFile, Quiz, Quiz_Question
from django.forms import inlineformset_factory

class QuizForm(forms.ModelForm):

    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Start Time"
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="End Time"
    )

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'start_time', 'end_time', 'is_public', 'price', 'shuffle_questions']

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = Quiz_Question
        exclude = ['quiz']

QuizQuestionFormSet = inlineformset_factory(
    Quiz, Quiz_Question, form=QuizQuestionForm,
    extra=1, can_delete=True
)

class UploadQuizFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        # fields = ['title', 'description', 'institution', 'start_time', 'end_time', 'is_public', 'price', 'shuffle_questions', 'file']


class PasscodeForm(forms.Form):
    passcode = forms.CharField(label='Enter Passcode', max_length=20)
