# quiz/utils.py
import docx
import pandas as pd
from .models import Quiz, Question, Option
from django.utils.text import slugify

def parse_word_file(file_path, user):
    document = docx.Document(file_path)
    quiz = Quiz.objects.create(title=f"Word Quiz {user.username}", created_by=user)
    current_question = None

    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            if text.endswith('?'):
                current_question = Question.objects.create(quiz=quiz, text=text)
            elif current_question:
                is_correct = text.startswith('*')
                option_text = text[1:].strip() if is_correct else text
                Option.objects.create(question=current_question, text=option_text, is_correct=is_correct)

def parse_excel_file(file_path, user):
    df = pd.read_excel(file_path)
    quiz = Quiz.objects.create(title=f"Excel Quiz {user.username}", created_by=user)

    for _, row in df.iterrows():
        question_text = row.get('Question')
        if pd.notna(question_text):
            question = Question.objects.create(quiz=quiz, text=question_text)
            for i in ['A', 'B', 'C', 'D']:
                option_col = f"Option_{i}"
                correct_col = f"Correct"
                option_text = row.get(option_col)
                if pd.notna(option_text):
                    is_correct = str(row.get(correct_col)).strip().upper() == i
                    Option.objects.create(question=question, text=option_text, is_correct=is_correct)
