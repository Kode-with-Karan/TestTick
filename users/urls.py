
# users/urls.py
from django.urls import path
from .views import register, login_view, logout_view, mark_notification_read, get_unread_notifications

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/unread/', get_unread_notifications, name='get_unread_notifications'),

]

