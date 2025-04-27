# quiz/models.py
from django.db import models
from institutions.models import Institution
from users.models import User
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    shuffle_questions = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 👈 Add this line


    def __str__(self):
        return self.title

class Quiz_Question(models.Model):

    CORRECT_OPTION = (
        ('options_A', 'Options A'),
        ('options_B', 'Options B'),
        ('options_C', 'Options C'),
        ('options_D', 'Options D'),
    )

    quiz = models.ForeignKey(Quiz, related_name='quiz_questions', on_delete=models.CASCADE)
    question = models.TextField()
    options_A = models.CharField(max_length=500)
    options_B = models.CharField(max_length=500)
    options_C = models.CharField(max_length=500)
    options_D = models.CharField(max_length=500)
    is_correct = models.CharField(max_length=20, choices=CORRECT_OPTION)


    def __str__(self):
        return self.question[:50]


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]

class StudentQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"

# quiz/models.py
class UploadedFile(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='quiz_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed = models.BooleanField(default=False)


class UsersAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='solved_questions', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.quiz}"
    
class Quiz_UserAnswer(models.Model):

    CORRECT_OPTION = (
        ('options_A', 'Options A'),
        ('options_B', 'Options B'),
        ('options_C', 'Options C'),
        ('options_D', 'Options D'),
    )

    user_answer = models.ForeignKey(UsersAnswer, related_name='quiz_user_answer', on_delete=models.CASCADE)
    question = models.TextField()
    options_A = models.CharField(max_length=500)
    options_B = models.CharField(max_length=500)
    options_C = models.CharField(max_length=500)
    options_D = models.CharField(max_length=500)
    is_selected = models.CharField(max_length=20, choices=CORRECT_OPTION)
    is_correct = models.CharField(max_length=20, choices=CORRECT_OPTION)


    def __str__(self):
        return self.question[:50]

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)


class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    session_id = models.IntegerField(default=0)
    started = models.BooleanField(default=False)
    current_question_index = models.IntegerField(default=0)
    current_question_start_time = models.DateTimeField(null=True, blank=True)

class StudentAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Quiz_Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    time_taken = models.FloatField()  # in seconds