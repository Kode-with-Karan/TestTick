# dashboard/urls.py
from django.urls import path
from .views import student_dashboard, institution_dashboard, approve_student, remove_student

urlpatterns = [
    path('student/', student_dashboard, name='student_dashboard'),
    path('students/<int:student_id>/approve/', approve_student, name='approve_student'),
    path('students/<int:student_id>/remove/', remove_student, name='remove_student'),

    path('institution/', institution_dashboard, name='institution_dashboard'),
]

