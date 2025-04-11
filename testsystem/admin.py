# testsystem/admin.py
from django.contrib import admin
from .models import TestSchedule, TestResult

admin.site.register(TestSchedule)
admin.site.register(TestResult)
