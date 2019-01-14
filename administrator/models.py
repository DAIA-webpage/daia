# coding=utf-8
from django.db import models
from PIL import Image
from .security import security_model
# Create your models here.

class User(models.Model):
    POSITION = (
        ('기장', '기장'),
        ('부기장', '부기장'),
        ('음성처리 팀장', '음성처리 팀장'),
        ('비젼인식 팀장', '비젼인식 팀장'),
        ('비젼생성 팀장','비젼생성 팀장'),
        ('총무', '총무'),
        ('회원', '회원')
    )
    student_id = models.IntegerField(db_column='Student_id', primary_key=True)
    name = models.CharField(db_column='Name', max_length=10, blank=True, null=True)
    major = models.CharField(db_column='Major', max_length=10, blank=True, null=True)
    class_field = security_model.class_field
    e_mail = models.CharField(db_column='E_Mail', max_length=30, blank=True, null=True)
    password = security_model.password
    phone = models.IntegerField(db_column='Phone', blank=True, null=True)
    github = models.CharField(db_column='Github', max_length=30, blank=True, null=True)
    introduction = models.CharField(db_column='Introduction', max_length=100, blank=True, null=True)
    sns_address = models.CharField(db_column='SNS_address', max_length=50, blank=True, null=True)
    auth_code = security_model.auth_code
    image = models.ImageField(upload_to='member', null=True, blank=True)
    position = models.CharField(db_column='Position', choices=POSITION, max_length=50, null=True, blank=True)

    '''
    #https://stackoverflow.com/questions/15140483/django-imagefield-setting-a-fixed-width-and-height?lq=1
    # for resize image
    # django image resize라는 키워드로 검색했습니당
    '''
    def save(self):
        if self.image:
            super(User, self).save()
            image = Image.open(self.image)
            size = (150, 150)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.image.path)
        super(User, self).save()

    #def __str__(self):
    def  __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(User, self).delete(*args, **kwargs)
        
class MainImage(models.Model):
    image1 = models.ImageField(upload_to='mainimage1/%Y/%m/%d/img', null=True, blank=True)
    image2 = models.ImageField(upload_to='mainimage2/%Y/%m/%d/img', null=True, blank=True)