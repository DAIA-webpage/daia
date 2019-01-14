# coding=utf-8
from django import forms
from .models import UserRequest
from administrator.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['student_id', 'name', 'major', 'e_mail', 'password',
                  'phone', 'github', 'introduction', 'sns_address',
                  ]

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserRequest
        fields = ['student_id', 'password']
    
        
class InfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['student_id', 'name', 'major', 'class_field', 'e_mail', 'password', 'phone', 'github', 'introduction', 'image','position']