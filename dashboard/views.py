# dashboard/views.py
from django.shortcuts import render
from users.models import User
from institutions.models import Institution
from django.contrib.auth.decorators import login_required
from results.models import TestSummary
from users.models import Notification

def student_dashboard(request):

    testSummary = TestSummary.objects.filter(user = request.user)
    notifications = Notification.objects.filter(user = request.user)
    unread_count = notifications.filter(read=False).count()

    return render(request, 'dashboard/student_dashboard.html', {'testSummary': testSummary, 'notifications': notifications, 'unread_count':unread_count})

@login_required
def institution_dashboard(request):
    institution = Institution.objects.filter(user=request.user).first()
    return render(request, 'dashboard/institution_dashboard.html', {'institution': institution})

