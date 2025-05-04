# dashboard/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from users.models import User
from institutions.models import Institution, Student
from django.contrib.auth.decorators import login_required
from results.models import TestSummary
from users.models import Notification
from django.db.models import Avg


@login_required
def student_dashboard(request):

    testSummary = TestSummary.objects.filter(user = request.user)
    notifications = Notification.objects.filter(user = request.user)
    unread_count = notifications.filter(read=False).count()

    return render(request, 'dashboard/student_dashboard.html', {'testSummary': testSummary, 'notifications': notifications, 'unread_count':unread_count})

@csrf_exempt
def approve_student(request, student_id):
    if request.method == 'POST':
        try:
            student = Student.objects.get(id=student_id)
            student.is_approved = True
            student.save()
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def remove_student(request, student_id):
    if request.method == 'POST':
        try:
            student = Student.objects.get(id=student_id)
            student.is_removed = True
            student.save()
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def institution_dashboard(request):
    institution =Institution.objects.filter(user=request.user).first()
    students = Student.objects.filter(institution=institution, is_approved = True)
    # testSummaries = TestSummary.objects.filter(institution=institution)
    students_request = Student.objects.filter(institution=institution, is_approved = False, is_removed = False)

    for student in students:
        print(student)
        testSummaries = TestSummary.objects.filter(institution=institution, user = student.user)
        if testSummaries:
            student.last_quiz = testSummaries.last().date_taken
            print(testSummaries.last().date_taken)
            student.quiz_attempt = testSummaries.count()
            averages = testSummaries.aggregate(
                avg_score=Avg('score'),
                avg_percentage=Avg('percentage'),
                avg_correct=Avg('correct_answers'),
                avg_total_question=Avg('total_questions'),
                avg_wrong=Avg('wrong_answers'),
                avg_skipped=Avg('skipped_questions')
            )
            student.avg_quiz_total = averages['avg_total_question']
            student.avg_quiz_correct= averages['avg_correct']
            student.avg_quiz_score= averages['avg_score']
            student.avg_quiz_persentage= averages['avg_percentage']
            student.save()


    return render(request, 'dashboard/institution_dashboard.html', {'institution': institution, 'students':students, 'students_request':students_request})

