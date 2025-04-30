# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import RegisteredUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            RegisteredUser.objects.create(
                username=username,
                email=email,
                role=role,
                password1=password1,
                password2=password2
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