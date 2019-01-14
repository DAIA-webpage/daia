from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^administrator/$', views.administrator, name='administrator'),
    url(r'^administrator/(?P<userRequest_student_id>\d+)/okay/$', views.okay, name='okay'),
    url(r'^administrator/(?P<user_student_id>\d+)/detail/$',views.detail,name='detail'),
    url(r'^administrator/(?P<user_student_id>\d+)/modify/$',views.modify,name='modify'),
    url(r'^administrator/mainImage_edit/$',views.mainImage_edit,name='mainImage_edit'),
    #url(r'^administrator/mainImage_detail/$',views.mainImage_detail,name='mainImage_detail'),
]
