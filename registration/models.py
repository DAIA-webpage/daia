# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .security import security_model

class UserRequest(models.Model):
    student_id = models.IntegerField(db_column='Student_id', primary_key=True)
    name = models.CharField(db_column='Name', max_length=10, blank=True, null=True)
    major = models.CharField(db_column='Major', max_length=10, blank=True, null=True)
    e_mail = models.CharField(db_column='E_Mail', max_length=30, blank=True, null=True)
    password = security_model.password
    phone = models.IntegerField(db_column='Phone', blank=True, null=True)
    github = models.CharField(db_column='Github', max_length=30, blank=True, null=True)
    introduction = models.CharField(db_column='Introduction', max_length=100, blank=True, null=True)
    sns_address = models.CharField(db_column='SNS_address', max_length=50, blank=True, null=True)
