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
