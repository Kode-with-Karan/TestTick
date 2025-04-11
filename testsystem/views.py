# testsystem/views.py
from django.shortcuts import render
from .models import TestSchedule

def test_schedule_list(request):
    schedules = TestSchedule.objects.all()
    return render(request, 'testsystem/schedule_list.html', {'schedules': schedules})

