# institutions/views.py
from django.shortcuts import render
from .models import Institution

def institution_list(request):
    institutions = Institution.objects.all()
    return render(request, 'institutions/institution_list.html', {'institutions': institutions})

