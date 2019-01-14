# coding=utf-8
from django import forms
from .models import Gallary,ProjectBoard, SeminarBoard, NewsBoard, NoticeBoard

class GallaryForm(forms.ModelForm):
    class Meta:
        model = Gallary
        fields = ('title','content')

class ProjectBoardForm(forms.ModelForm):
    class Meta:
        model = ProjectBoard
        fields = ('title','content','project_member','process','image','file')

class SeminarBoardForm(forms.ModelForm):
    class Meta:
        model = SeminarBoard
        fields = ('title','content','image','file')

# 다른 곳에서는 Notice에서 news로 이름을 정정함. 이를 참고할 것
class NewsBoardForm(forms.ModelForm):
    class Meta:
        model = NewsBoard
        fields = ('title','content','image','file')

class NoticeBoardForm(forms.ModelForm):
    class Meta:
        model = NoticeBoard
        fields = ('title','content','image','file')