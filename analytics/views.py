from django.shortcuts import render
from .models import QuestionPerformance, InstitutionStats
from django.contrib.auth.decorators import login_required
from institutions.models import Institution
from users.models import User

@login_required
def institution_analytics(request):
    if hasattr(request.user, 'institution'):
        stats = InstitutionStats.objects.filter(institution=request.user.institution).first()
        questions = QuestionPerformance.objects.filter(
            question__quiz__created_by__institution=request.user.institution
        )
        return render(request, 'analytics/institution_dashboard.html', {
            'stats': stats,
            'questions': questions
        })
    return render(request, 'analytics/no_access.html')
