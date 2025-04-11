
# quiz/admin.py
from django.contrib import admin
from .models import Quiz, Question, Option, StudentQuiz

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(StudentQuiz)
