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
    path('is_session_active/<int:session_id>/', views.is_session_active, name='is_session_active'),
    path('api/leaderboard/<int:session_id>/', views.leaderboard_api, name='leaderboard_api'),

    path('start_live_quiz', views.start_live_quiz, name='start_live_quiz'),
    path('show_live_quiz_student/<int:session_id>/<int:quiz_id>', views.show_live_quiz_student, name='show_live_quiz_student'),
    path('get_participants/<int:session_id>/', views.get_participants_ajax, name='get_participants_ajax'),

]
