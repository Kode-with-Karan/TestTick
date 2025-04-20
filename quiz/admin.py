
# quiz/admin.py
from django.contrib import admin
from .models import Quiz, Question, Option, StudentQuiz, UploadedFile, UserAnswer, Quiz_Question, Quiz_UserAnswer, UsersAnswer

class QuizQuestionInline(admin.TabularInline):  # or admin.StackedInline
    model = Quiz_Question
    extra = 1  # Number of empty forms to show

class UserAnswerInline(admin.TabularInline):  # or admin.StackedInline
    model = Quiz_UserAnswer
    extra = 1  # Number of empty forms to show

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]

@admin.register(UsersAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    inlines = [UserAnswerInline]

# admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(StudentQuiz)
admin.site.register(UserAnswer)
admin.site.register(UploadedFile)
admin.site.register(Quiz_Question)

