# quiz/forms.py
from django import forms
from .models import UploadedFile

class UploadQuizFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        # fields = ['title', 'description', 'institution', 'start_time', 'end_time', 'is_public', 'price', 'shuffle_questions', 'file']
