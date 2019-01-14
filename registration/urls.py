from django.conf.urls import include, url
from .security import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.loginin, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^info/$', views.info, name='info'),
    ]
