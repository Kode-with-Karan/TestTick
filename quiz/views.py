
# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import os
from .models import UploadedFile, Quiz, Quiz_Question, QuizSession, StudentAnswer, StudentQuiz, Quiz_UserAnswer, UsersAnswer
from .forms import UploadQuizFileForm, QuizForm, QuizQuestionFormSet, PasscodeForm
from .utils import parse_word_file, parse_excel_file
from institutions.models import Institution  
from results.models import TestSummary
from users.models import User
import re


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

@login_required
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


@login_required
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


@login_required
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

def set_multi_quiz(request):

    return render(request, 'quiz/upload_file.html')

# Start the quiz
def start_quiz(request, quiz_id):

    last_quiz_session = QuizSession.objects.latest('id')
    # quiz_session = last_quiz_session.id
    session_id = int(last_quiz_session.id)+1


    session = QuizSession.objects.create(
        quiz_id=quiz_id,
        session_id = session_id,
        started=True,
        current_question_start_time=timezone.now()
    )
    return redirect('institution_dashboard', session_id=session.id)

# Student joins the quiz
def student_quiz(request, session_id):

    if QuizSession.objects.filter(session_id = session_id):
        return render(request, 'quiz/student_quiz.html', {'session_id': session_id})

    return render(request, 'quiz/quiz_unavailale.html', {'session_id': session_id})
     
    

# API for live question update
def quiz_status_api(request, session_id):
    session = QuizSession.objects.get(session_id=session_id)
    # print(session)
    time_elapsed = (timezone.now() - session.current_question_start_time).seconds

    if time_elapsed >= 20:
        # print(time_elapsed)
        session.current_question_index += 1
        session.current_question_start_time = timezone.now()
        session.save()

    questions = session.quiz.quiz_questions.all()
    if session.current_question_index >= len(questions):
        return JsonResponse({'end': True})

    question = questions[session.current_question_index]
    data = {
        'question': question.question,
        'options': {
            'A': question.options_A,
            'B': question.options_B,
            'C': question.options_C,
            'D': question.options_D,
        },
        'time_left': 20 - time_elapsed,
        'question_id': question.id,
    }
    # print(data)
    return JsonResponse(data)

# Submit Answer
def submit_answer(request):
    
    if request.method == 'POST':
        user = request.user
        session_id = request.POST.get('session_id')
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('selected_option')
        time_taken = request.POST.get('time_taken')

        session = QuizSession.objects.get(session_id=session_id)
        # quiz = Quiz.objects.get(id = session.quiz.id)
        # users_answer = UsersAnswer.objects.create(user=user, quiz=quiz)

        # question = Question.objects.get(id=question_id)
        question = session.quiz.quiz_questions.get(id= question_id)

        print(question.id)
        print("options_"+selected_option)
        is_correct = ("options_"+selected_option == question.is_correct)

        # question = Quiz_Question.objects.get(id=80)

        StudentAnswer.objects.create(
            user=user,
            session=session,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            time_taken=time_taken
        )

        # Quiz_UserAnswer.objects.create(
        #     user_answer=users_answer,
        #     question=question.question,
        #     options_A=question.options_A,
        #     options_B=question.options_B,
        #     options_C=question.options_C,
        #     options_D=question.options_D,
        #     is_correct = question.is_correct,
        #     is_selected="options_"+selected_option  # what user selected
        # )

        return JsonResponse({'success': True})

# Institution Dashboard
def institution_dashboard(request, session_id):
    return render(request, 'quiz/institution_dashboard.html', {'session_id': session_id})

# API for live leaderboard
def leaderboard_api(request, session_id):
    session = QuizSession.objects.get(session_id=session_id)
    answers = StudentAnswer.objects.filter(session=session)
    print(answers)

    leaderboard = {}

    for ans in answers:
        user_id = ans.user.id
        if user_id not in leaderboard:
            leaderboard[user_id] = {
                'username': ans.user.username,
                'correct': 0,
                'total_time': 0
            }
        if ans.is_correct:
            leaderboard[user_id]['correct'] += 1
            leaderboard[user_id]['total_time'] += ans.time_taken

    ranked = sorted(leaderboard.values(), key=lambda x: (-x['correct'], x['total_time']))
    ranked = [{'username': 'karan', 'correct': 1, 'total_time': 1.726}, {'username': 'karan2', 'correct': 0, 'total_time': 0}]
    # print()
    return JsonResponse({'leaderboard': ranked})

from django.db.models import Max

def start_live_quiz(request):
    quizzes = Quiz.objects.all()

    last_quiz_session = QuizSession.objects.latest('id')
    # quiz_session = last_quiz_session.id
    print(last_quiz_session.id)

    
    # text = str(quiz_session)
    
    # import re
    # match = re.search(r'\((\d+)\)', text)
    # number = match.group(1) if match else None

    return render(request, 'quiz/start_live_quiz.html', {'quizzes': quizzes, 'session_id': int(last_quiz_session.id)+1 })