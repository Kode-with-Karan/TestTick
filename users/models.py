# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from institutions.models import Institution

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('student', 'Student'),
#         ('institution', 'Institution'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('institution', 'Institution'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)

class RegisteredUser(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('institution', 'Institution'),
    )
    username = models.CharField()
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    password1 = models.CharField()
    password2 = models.CharField()


    def __str__(self):
        return self.username
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:50]}"