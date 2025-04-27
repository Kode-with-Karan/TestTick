from django.contrib import admin
from .models import TestSummary

# @admin.register(StudentAnswer)
# class StudentAnswerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'question', 'selected_option', 'is_correct', 'answered_at')
#     search_fields = ('user__username', 'question__text')

@admin.register(TestSummary)
class TestSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_name', 'percentage', 'date_taken')
    list_filter = ('test_name', 'date_taken')
