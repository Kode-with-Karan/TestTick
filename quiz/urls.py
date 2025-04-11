# quiz/urls.py
from django.urls import path
from .views import quiz_list, quiz_detail
from .views import upload_quiz_file

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:pk>/', quiz_detail, name='quiz_detail'),
    path('upload/', upload_quiz_file, name='upload_quiz_file'),
]
