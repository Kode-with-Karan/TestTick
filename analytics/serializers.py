from rest_framework import serializers
from .models import QuestionPerformance, UserActivityLog, InstitutionStats

class QuestionPerformanceSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = QuestionPerformance
        fields = ['id', 'question_text', 'times_attempted', 'times_correct', 'success_rate']

    def get_success_rate(self, obj):
        return obj.success_rate()

class UserActivityLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserActivityLog
        fields = ['id', 'username', 'action', 'timestamp']

class InstitutionStatsSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = InstitutionStats
        fields = ['id', 'institution_name', 'total_tests', 'total_students', 'average_score']
