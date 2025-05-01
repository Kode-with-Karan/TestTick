# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import RegisteredUser
from institutions.models import Institution

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             role = form.cleaned_data.get('role')
#             password1 = form.cleaned_data.get('password1')
#             password2 = form.cleaned_data.get('password2')

#             RegisteredUser.objects.create(
#                 username=username,
#                 email=email,
#                 role=role,
#                 password1=password1,
#                 password2=password2
#             )
#             login(request, user)
#             return redirect('student_dashboard')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {'form': form})


def register(request):
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         role = form.cleaned_data.get('role')

    #         if role == 'institution':
    #             institution = Institution.objects.create(
    #                 user=user,
    #                 name=form.cleaned_data.get('institution_name'),
    #                 institution_type=form.cleaned_data.get('institution_type')
    #             )
    #         elif role == 'student':
    #             institution = form.cleaned_data.get('select_institution')
    #             # optional: link institution to user via FK if needed

    #         user.save()
    #         login(request, user)
    #         return redirect('student_dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.save()

            if role == 'institution':
                Institution.objects.create(
                    user=user,
                    name=form.cleaned_data.get('institution_name'),
                    institution_type=form.cleaned_data.get('institution_type'),
                )
            elif role == 'student':
                selected_institution = form.cleaned_data.get('select_institution')
                from institutions.models import Student  # Import here or top
                Student.objects.create(
                    user=user,
                    institution=selected_institution,
                )

            login(request, user)
            return redirect('student_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard')  # or wherever you want after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home') 