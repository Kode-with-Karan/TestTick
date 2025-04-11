# quiz/forms.py
from django import forms
from .models import UploadedFile

class UploadQuizFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
