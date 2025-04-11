# institutions/models.py
from django.db import models
from users.models import User

class Institution(models.Model):
    INSTITUTION_TYPE_CHOICES = (
        ('school', 'School'),
        ('coaching', 'Coaching'),
        ('college', 'College'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution_profile')
    name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPE_CHOICES)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_institution_type_display()})"

