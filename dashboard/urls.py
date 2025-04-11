# dashboard/urls.py
from django.urls import path
from .views import student_dashboard, institution_dashboard

urlpatterns = [
    path('student/', student_dashboard, name='student_dashboard'),
    path('institution/', institution_dashboard, name='institution_dashboard'),
]

