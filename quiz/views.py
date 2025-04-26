
# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from .models import UploadedFile, Quiz, Quiz_Question, Option, UserAnswer, StudentQuiz, Quiz_UserAnswer, UsersAnswer
from .forms import UploadQuizFileForm, QuizForm, QuizQuestionFormSet, PasscodeForm
from .utils import parse_word_file, parse_excel_file
from institutions.models import Institution  
from results.models import TestSummary
from users.models import User


def quiz_code(request):

    form = PasscodeForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data['passcode']
            print(code)
            split_code = [code[i:i+2] for i in range(0, len(code), 2)]
            print(split_code)
            institution = get_object_or_404(Institution, pk=split_code[1])
            print(institution)
            user = get_object_or_404(User, pk=split_code[2])
            print(user)
            quiz = get_object_or_404(Quiz, pk=split_code[0], institution=institution, created_by= user)
            return redirect('solve_quiz', pk=quiz.pk)

    return render(request, 'quiz/enter_passcode.html', {'form': form, 'error': error})

# def quiz_passcode_view(request):
#     form = PasscodeForm(request.POST or None)
#     error = None

#     if request.method == 'POST':
#         if form.is_valid():
#             code = form.cleaned_data['passcode']
#             try:
#                 quiz = Quiz.objects.get(passcode=code)
#                 return redirect('quiz_detail', quiz_id=quiz.id)
#             except Quiz.DoesNotExist:
#                 error = "Invalid passcode. Try again."

#     return render(request, 'quiz/enter_passcode.html', {'form': form, 'error': error})


def get_default_institution(user):
    return Institution.objects.filter(user=user).first()  # assuming you have a relation

# @login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        formset = QuizQuestionFormSet(request.POST)

        print(get_default_institution(request.user))

        


        quiz_file = request.FILES.get('quiz_file')  # 👈 Get the uploaded file if any

        if quiz_file:
            uploaded = UploadedFile.objects.create(
                uploader=request.user,
                file=quiz_file,
                parsed=False
            )

            file_path = uploaded.file.path
            ext = os.path.splitext(file_path)[1]

            if ext in ['.docx', '.doc']:
                parse_word_file(file_path, request.user,
                                 title = request.POST.get("title"), 
                                 description =  request.POST.get("description"),
                                 is_public = ('True' if request.POST.get("is_public") else 'False'), 
                                 start_time = request.POST.get("start_time"), 
                                 end_time = request.POST.get("end_time"), 
                                 shuffle_questions = ('True' if request.POST.get("shuffle_questions") else 'False'),
                                 price = request.POST.get("price"),
                                 )
            elif ext in ['.xlsx', '.xls']:
                parse_excel_file(file_path, request.user,
                                 title = request.POST.get("title"), 
                                 description =  request.POST.get("description"),
                                 is_public = ('True' if request.POST.get("is_public") else 'False'), 
                                 start_time = request.POST.get("start_time"), 
                                 end_time = request.POST.get("end_time"), 
                                 shuffle_questions = ('True' if request.POST.get("shuffle_questions") else 'False'),
                                 price = request.POST.get("price"),
                                 )

            uploaded.parsed = True
            uploaded.save()

            messages.success(request, "Quiz created from uploaded file.")
            return redirect('quiz_list')  # Change to your actual quiz list page

        if form.is_valid() and formset.is_valid():
            quiz = form.save(commit=False)
            quiz.institution = get_default_institution(request.user)
            quiz.created_by = request.user
            quiz.save()
            formset.instance = quiz
            formset.save()

            messages.success(request, "Quiz created manually.")
            return redirect('quiz_list')

    else:
        form = QuizForm()
        formset = QuizQuestionFormSet()

    return render(request, 'quiz/create_quiz.html', {
        'form': form,
        'formset': formset,
    })

# def create_quiz(request):
#     if request.method == 'POST':
#         form = QuizForm(request.POST)
#         formset = QuizQuestionFormSet(request.POST, prefix='form')  # 💡 Add prefix here

#         if form.is_valid() and formset.is_valid():
#             quiz = form.save()
#             questions = formset.save(commit=False)
#             for q in questions:
#                 q.quiz = quiz
#                 q.save()
#             return redirect('home')

#     else:
#         form = QuizForm()
#         formset = QuizQuestionFormSet(prefix='form')  # 💡 Add prefix here too

#     return render(request, 'quiz/create_quiz.html', {'form': form, 'formset': formset})


# @login_required
def solve_quiz(request, pk):

    if request.user.is_authenticated:
        quiz = get_object_or_404(Quiz, pk=pk)

        # if quiz.start_time and quiz.end_time:
        #     now = timezone.now()
        #     if now < quiz.start_time or now > quiz.end_time:
        #         return render(request, 'quiz/quiz_unavailable.html', {'quiz': quiz})

        questions = quiz.quiz_questions.all()

        # print(questions)

        if quiz.shuffle_questions:
            questions = list(questions.order_by('?'))

        if request.method == 'POST':
            score = 0

            # Create the UsersAnswer record for this attempt
            users_answer = UsersAnswer.objects.create(user=request.user, quiz=quiz)

            for question in questions:
                selected = request.POST.get(str(question.id))  # should be 'options_A', etc.
                correct = question.is_correct

                if selected:
                    is_correct = selected == correct
                    if is_correct:
                        score += 1

                    Quiz_UserAnswer.objects.create(
                        user_answer=users_answer,
                        question=question.question,
                        options_A=question.options_A,
                        options_B=question.options_B,
                        options_C=question.options_C,
                        options_D=question.options_D,
                        is_correct = correct,
                        is_selected=selected  # what user selected
                    )

            
            # Save score separately
            StudentQuiz.objects.update_or_create(
                quiz=quiz,
                student=request.user,
                defaults={'score': score, 'completed': True}
            )

            return HttpResponseRedirect(reverse('quiz_result', args=[quiz.pk]))
    else:
        return redirect

    return render(request, 'quiz/solve_quiz.html', {
        'quiz': quiz,
        'questions': questions,
    })


# @login_required
def quiz_result(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    # Fetch the user's answer record for this quiz
    users_answer = UsersAnswer.objects.filter(user=request.user, quiz=quiz).last()

    if not users_answer:
        return render(request, 'quiz/quiz_not_taken.html', {'quiz': quiz})
    
    
    all_questions = Quiz_Question.objects.filter(quiz=quiz)
    all_answers = Quiz_UserAnswer.objects.filter(user_answer=users_answer)

    print(all_answers)

    total_questions = all_questions.count()
    correct_answers = 0
    wrong_answers = 0
    skipped_questions = 0  # If none selected

    for ans in all_answers:
        if not ans.is_selected:
            skipped_questions += 1
        elif ans.is_selected == ans.is_correct:
            correct_answers += 1
        else:
            wrong_answers += 1

    skipped_questions = total_questions-(correct_answers+wrong_answers)  # If none selected
    score = correct_answers  # Assuming 1 point per correct answer
    percentage = (correct_answers / total_questions * 100) if total_questions else 0

    # Get all the submitted answers linked to this quiz attempt
    submitted_answers = users_answer.quiz_user_answer.all()
    print(submitted_answers[0].is_selected)

    # Optional: Calculate score (assuming 'is_correct' means the correct option, and we compare with selected)

    for ans in submitted_answers:
        print(ans.is_correct, ans.is_selected , ans.is_correct == ans.is_selected)

    # print()

    TestSummary.objects.create(
        user = request.user,
        institution = get_default_institution(request.user),
        test_name = quiz,
        total_questions = total_questions,
        correct_answers = correct_answers,
        wrong_answers =wrong_answers,
        skipped_questions = skipped_questions,
        score = score,
        percentage = percentage,
        # time_taken = timezone.now().time(),
    )

    # correct_count = sum(1 for ans in submitted_answers if ans.is_correct == ans.is_selected)
    # # correct_count = 1
    # total_questions = submitted_answers.count()
    # score = (correct_count / total_questions) * 100 if total_questions else 0

    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'users_answer': users_answer,
        'submitted_answers': submitted_answers,
        'submitted_answers_count': correct_answers+wrong_answers,
        'correct_answers': correct_answers,
        'wrong_answers': wrong_answers,
        'skipped_questions': skipped_questions,
        'total_questions': total_questions,
        'score': score,
        'percentage':percentage,
        'result_message': "Great job!" if score >= 70 else "Keep trying!",
    })

# @login_required
# def solve_quiz(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk)

#     # Restrict access based on time
#     # if timezone.now() < quiz.start_time or timezone.now() > quiz.end_time:
#     #     return render(request, 'quiz/quiz_unavailable.html', {'quiz': quiz})

#     questions = quiz.questions.all().prefetch_related('options')

#     if quiz.shuffle_questions:
#         questions = list(questions.order_by('?'))

#     if request.method == 'POST':
#         score = 0
#         total_questions = len(questions)

#         for question in questions:
#             selected_option_id = request.POST.get(str(question.id))
#             if selected_option_id:
#                 selected_option = Option.objects.get(pk=selected_option_id)
#                 is_correct = selected_option.is_correct
#                 UserAnswer.objects.create(
#                     user=request.user,
#                     question=question,
#                     selected_option=selected_option,
#                     is_correct=is_correct
#                 )
#                 if is_correct:
#                     score += 1

#         StudentQuiz.objects.update_or_create(
#             quiz=quiz,
#             student=request.user,
#             defaults={'score': score, 'completed': True}
#         )

#         return HttpResponseRedirect(reverse('quiz_result', args=[quiz.pk]))

#     return render(request, 'quiz/solve_quiz.html', {
#         'quiz': quiz,
#         'questions': questions
#     })

# @login_required
# def quiz_result(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk)
#     student_quiz = StudentQuiz.objects.filter(quiz=quiz, student=request.user).first()
#     user_answers = UserAnswer.objects.filter(user=request.user, question__quiz=quiz)

#     print(user_answers)

#     return render(request, 'quiz/quiz_result.html', {
#         'quiz': quiz,
#         'student_quiz': student_quiz,
#         'user_answers': user_answers,
#     })

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