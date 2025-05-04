from django.shortcuts import render
from users.models import Notification


def home(request):
    notifications = ""
    try:
        notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')

    except Exception as e:
        print(e)
    return render(request, 'pages/home.html',{'notifications': notifications})

def about(request):
    return render(request, 'pages/about.html')
def service(request):
    return render(request, 'pages/service.html')
def menu(request):
    return render(request, 'pages/menu.html')
def event(request):
    return render(request, 'pages/event.html')
def contact(request):
    return render(request, 'pages/contact.html')
