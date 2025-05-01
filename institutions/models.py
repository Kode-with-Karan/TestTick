# institutions/models.py
from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model

# User = get_user_model()

class Institution(models.Model):
    # from users.models import User
    INSTITUTION_TYPE_CHOICES = (
        ('school', 'School'),
        ('coaching', 'Coaching'),
        ('college', 'College'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution_profile')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='institution_profile')
    name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPE_CHOICES)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_institution_type_display()})"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='students')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.institution.name}"

