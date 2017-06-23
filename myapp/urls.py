from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        #url(r'^(?P<course_no>\w+[\s]*\w+)/$', views.detail, name='detail'),
        url(r'^(?P<course_no>\d+)/$', views.detail, name='detail'),
        url(r'topics/$', views.topics, name='topics'),
        url(r'addtopic/$', views.addtopic, name='addtopic'),
        url(r'topics/(?P<topic_id>\d+)$', views.topicdetail, name='topicdetail'),
        url(r'register/$', views.register, name='register'),
        url(r'login/$', views.user_login, name='user_login'),
        url(r'logout/$', views.user_logout, name='user_logout'),
        url(r'mycourses/$', views.mycourses, name='mycourses'),
]