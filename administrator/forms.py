# coding=utf-8
from django import forms
from .models import User, MainImage

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
'''
class NameForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), initial='0')
    email = forms.CharField(widget=forms.TextInput(), initial='0')
    password = forms.CharField(widget=forms.TextInput(), initial='0')
    git = forms.CharField(widget=forms.TextInput(), initial='0')
    sns = forms.CharField(widget=forms.TextInput(), initial='0')
    student_id = forms.IntegerField(widget=forms.TextInput(), initial='0')
    phone_num = forms.IntegerField(widget=forms.TextInput(), initial='0')
    #image = forms.FileField(upload_to=None, max_length=100)
'''

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('student_id', 'name', 'major', 'class_field', 'e_mail', 'password', 'phone', 'github', 'introduction','auth_code','image','position')


class MainImageForm(forms.ModelForm):
    class Meta:
        model = MainImage
        fields ='image1', 'image2'
