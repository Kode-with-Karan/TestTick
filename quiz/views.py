
# quiz/views.py
from django.shortcuts import render, get_object_or_404
import os
from .models import UploadedFile, Quiz, Question, Option
from .forms import UploadQuizFileForm
from .utils import parse_word_file, parse_excel_file

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