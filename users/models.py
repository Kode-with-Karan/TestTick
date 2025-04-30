# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('institution', 'Institution'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

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