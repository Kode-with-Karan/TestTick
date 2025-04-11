from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_results, name='user_results'),
    path('download/', views.download_results_excel, name='download_results_excel'),
]
