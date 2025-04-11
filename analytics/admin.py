from django.contrib import admin
from .models import QuestionPerformance, UserActivityLog, InstitutionStats

@admin.register(QuestionPerformance)
class QuestionPerformanceAdmin(admin.ModelAdmin):
    list_display = ('question', 'times_attempted', 'times_correct', 'success_rate')

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'action')

@admin.register(InstitutionStats)
class InstitutionStatsAdmin(admin.ModelAdmin):
    list_display = ('institution', 'total_tests', 'total_students', 'average_score')
