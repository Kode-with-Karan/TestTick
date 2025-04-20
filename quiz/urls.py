# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('upload/', views.upload_quiz_file, name='upload_quiz_file'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:pk>/solve/', views.solve_quiz, name='solve_quiz'),
    path('<int:pk>/result/', views.quiz_result, name='quiz_result'),
]
