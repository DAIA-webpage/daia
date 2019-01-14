# coding=utf-8
from django.db import models
from django.utils import timezone

class Gallary(models.Model):
    title = models.CharField(db_column='Gallary_title', max_length=100,default="")
    content = models.TextField()
    origin_date = models.DateTimeField(db_column='Origin_date', blank=True, null=True)
    final_date = models.DateTimeField(db_column='Final_date', blank=True, null=True)
    writer_name = models.CharField(db_column='Writer_name', max_length=10, blank=True, null=True)
    writer_id = models.IntegerField(db_column='Writer_id', blank=True, null=True)


class Images(models.Model):
    post = models.ForeignKey(Gallary, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallary/%Y/%m/%d'
                              , null=True, blank=True)
    #def __str__(self):
    def __unicode__(self):
        return self.post.title+" Image"



# 프로젝트 게시판 table
class ProjectBoard(models.Model):
    title = models.CharField(db_column='Project_title', max_length=100,default="")
    content = models.TextField()
    project_member = models.CharField(db_column='Project_Member', max_length=200,default="")
    origin_date = models.DateTimeField(db_column='Origin_date', blank=True, null=True)
    final_date = models.DateTimeField(db_column='Final_date', blank=True, null=True)
    writer_name = models.CharField(db_column='Writer_name', max_length=10, blank=True, null=True)
    writer_id = models.IntegerField(db_column='Writer_id', blank=True, null=True)
    process = models.BooleanField()
    image = models.ImageField(upload_to='project/%Y/%m/%d/img', null=True, blank=True)
    file=models.FileField(upload_to='project/%Y/%m/%d/file', null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.file.delete()
        super(ProjectBoard, self).delete(*args, **kwargs)

# 세미나 자료 게시판 table
class SeminarBoard(models.Model):
    title = models.CharField(db_column='Title', max_length=100,default="")
    content = models.TextField()
    origin_date = models.DateTimeField(db_column='Origin_date', blank=True, null=True)
    final_date = models.DateTimeField(db_column='Final_date', blank=True, null=True)
    writer_name = models.CharField(db_column='Writer_name', max_length=10, blank=True, null=True)
    writer_id = models.IntegerField(db_column='Writer_id', blank=True, null=True)
    image = models.ImageField(upload_to='seminar/%Y/%m/%d/img', null=True, blank=True)
    file = models.FileField(upload_to='seminar/%Y/%m/%d/file', null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.file.delete()
        super(SeminarBoard, self).delete(*args, **kwargs)

# 다른 곳에서는 Notice에서 news로 이름을 정정함. 이를 참고할 것
class NoticeBoard(models.Model):
    title = models.CharField(db_column='Title', max_length=100,default="")
    origin_date = models.DateTimeField(db_column='Origin_date', blank=True, null=True)
    final_date = models.DateTimeField(db_column='Final_date', blank=True, null=True)
    writer_name = models.CharField(db_column='Writer_name', max_length=10, blank=True, null=True)
    writer_id = models.IntegerField(db_column='Writer_id', blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='notice/%Y/%m/%d/img', null=True, blank=True)
    file = models.FileField(upload_to='notice/%Y/%m/%d/file', null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.file.delete()
        super(NoticeBoard, self).delete(*args, **kwargs)

class NewsBoard(models.Model):
    title = models.CharField(db_column='Title', max_length=100,default="")
    origin_date = models.DateTimeField(db_column='Origin_date', blank=True, null=True)
    final_date = models.DateTimeField(db_column='Final_date', blank=True, null=True)
    writer_name = models.CharField(db_column='Writer_name', max_length=10, blank=True, null=True)
    writer_id = models.IntegerField(db_column='Writer_id', blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/%Y/%m/%d/img', null=True, blank=True)
    file = models.FileField(upload_to='news/%Y/%m/%d/file', null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.file.delete()
        super(NewsBoard, self).delete(*args, **kwargs)
