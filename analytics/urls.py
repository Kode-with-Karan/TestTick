from django.urls import path
from . import views
from .api_views import QuestionPerformanceList

urlpatterns = [
    path('institution/', views.institution_analytics, name='institution_analytics'),
    path('question-performance/', QuestionPerformanceList.as_view(), name='question-performance-list'),

]
