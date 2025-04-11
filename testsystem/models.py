# testsystem/models.py
from django.db import models
from quiz.models import Quiz
from users.models import User

class TestSchedule(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    scheduled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} ({self.start_time} - {self.end_time})"

class TestResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score})"
