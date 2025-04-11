from django.urls import path
from . import api_views

urlpatterns = [
    path('question-performance/', api_views.QuestionPerformanceList.as_view(), name='question-performance-list'),
    path('question-performance/pdf/', api_views.ExportQuestionPerformancePDF.as_view(), name='export-question-performance-pdf'),
    path('question-performance/csv/', api_views.ExportQuestionPerformanceCSV.as_view(), name='export-question-performance-csv'),
    path('institution-stats/pdf/', api_views.ExportInstitutionStatsPDF.as_view(), name='export-institution-stats-pdf'),
    path('institution-stats/csv/', api_views.ExportInstitutionStatsCSV.as_view(), name='export-institution-stats-csv'),

    path('user-activity/', api_views.UserActivityList.as_view(), name='api_user_activity'),
    path('institution-stats/', api_views.InstitutionStatsDetail.as_view(), name='api_institution_stats'),
]
