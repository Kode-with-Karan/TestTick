
# quiz/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from .models import UploadedFile, Quiz, Question, Option, UserAnswer, StudentQuiz
from .forms import UploadQuizFileForm
from .utils import parse_word_file, parse_excel_file


@login_required
def solve_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    # Restrict access based on time
    if timezone.now() < quiz.start_time or timezone.now() > quiz.end_time:
        return render(request, 'quiz/quiz_unavailable.html', {'quiz': quiz})

    questions = quiz.questions.all().prefetch_related('options')

    if quiz.shuffle_questions:
        questions = list(questions.order_by('?'))

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)

        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                selected_option = Option.objects.get(pk=selected_option_id)
                is_correct = selected_option.is_correct
                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )
                if is_correct:
                    score += 1

        StudentQuiz.objects.update_or_create(
            quiz=quiz,
            student=request.user,
            defaults={'score': score, 'completed': True}
        )

        return HttpResponseRedirect(reverse('quiz_result', args=[quiz.pk]))

    return render(request, 'quiz/solve_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def quiz_result(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student_quiz = StudentQuiz.objects.filter(quiz=quiz, student=request.user).first()
    user_answers = UserAnswer.objects.filter(user=request.user, question__quiz=quiz)

    print(user_answers)

    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'student_quiz': student_quiz,
        'user_answers': user_answers,
    })

def quiz_list(request):
    quizzes = Quiz.objects.filter(is_public=True)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})


def upload_quiz_file(request):
    if request.method == 'POST':
        form = UploadQuizFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploader = request.user
            uploaded_file.save()

            file_path = uploaded_file.file.path
            ext = os.path.splitext(file_path)[1]

            if ext in ['.docx', '.doc']:
                parse_word_file(file_path, request.user)
            elif ext in ['.xlsx', '.xls']:
                parse_excel_file(file_path, request.user)

            uploaded_file.parsed = True
            uploaded_file.save()

    else:
        form = UploadQuizFileForm()

    return render(request, 'quiz/upload_file.html', {'form': form})