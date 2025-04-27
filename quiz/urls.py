# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('upload/', views.upload_quiz_file, name='upload_quiz_file'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('code/', views.quiz_code, name='quiz_code'),
    path('<int:pk>/solve/', views.solve_quiz, name='solve_quiz'),
    path('<int:pk>/result/', views.quiz_result, name='quiz_result'),

    
    path('start_quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('join_quiz/<int:session_id>/', views.student_quiz, name='student_quiz'),
    path('api/quiz_status/<int:session_id>/', views.quiz_status_api, name='quiz_status_api'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('institution_dashboard/<int:session_id>/', views.institution_dashboard, name='institution_dashboard'),
    path('api/leaderboard/<int:session_id>/', views.leaderboard_api, name='leaderboard_api'),

    path('start_live_quiz', views.start_live_quiz, name='start_live_quiz'),
    
]
