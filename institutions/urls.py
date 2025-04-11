# institutions/urls.py
from django.urls import path
from .views import institution_list

urlpatterns = [
    path('', institution_list, name='institution_list'),
]

