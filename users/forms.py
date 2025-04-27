# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Add CSS classes to fields
        self.fields['username'].widget.attrs.update({'class': 'w-100 form-control p-3 border-primary bg-light'})
        self.fields['email'].widget.attrs.update({'class': 'w-100 form-control p-3 border-primary bg-light'})
        self.fields['role'].widget.attrs.update({'class': 'w-100 form-control p-3 border-primary bg-light'})
        self.fields['profile_image'].widget.attrs.update({'class': 'w-100 form-control p-3 border-primary bg-light'})
        self.fields['password1'].widget.attrs.update({'class': 'w-100 form-control p-3 border-primary bg-light'})
        self.fields['password2'].widget.attrs.update({'class': 'w-100 form-control p-3 border-primary bg-light'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'profile_image')

