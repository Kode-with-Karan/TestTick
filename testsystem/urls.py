
# testsystem/urls.py
from django.urls import path
from .views import test_schedule_list

urlpatterns = [
    path('', test_schedule_list, name='test_schedule_list'),
]
