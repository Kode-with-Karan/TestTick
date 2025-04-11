from django.contrib import admin
from .models import StudentAnswer, TestSummary

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'selected_option', 'is_correct', 'submitted_at')
    search_fields = ('student__username', 'question__text')

@admin.register(TestSummary)
class TestSummaryAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score_percentage', 'completed_at')
    list_filter = ('quiz', 'completed_at')
