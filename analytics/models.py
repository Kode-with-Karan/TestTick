# analytics/models.py
from django.db import models
from users.models import User
from quiz.models import Quiz, Question
from institutions.models import Institution

class QuestionPerformance(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    times_attempted = models.PositiveIntegerField(default=0)
    times_correct = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.question.text[:50]}..."

    def success_rate(self):
        if self.times_attempted == 0:
            return 0
        return round((self.times_correct / self.times_attempted) * 100, 2)

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

class InstitutionStats(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    total_tests = models.PositiveIntegerField(default=0)
    total_students = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.institution.name} - Stats"
