
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from quiz.models import Question  # Adjust this import based on your app structure

class StudentAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    test_name = models.CharField(max_length=200)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Q{self.question.id} - {'Correct' if self.is_correct else 'Wrong'}"


class TestSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_summaries')
    test_name = models.CharField(max_length=200)
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    wrong_answers = models.PositiveIntegerField()
    skipped_questions = models.PositiveIntegerField(default=0)
    score = models.FloatField()
    percentage = models.FloatField()
    time_taken = models.DurationField()  # Use timedelta to track time
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test_name} ({self.percentage:.2f}%)"
