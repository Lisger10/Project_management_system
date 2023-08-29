from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2', 'last_name', 'first_name'] 
    