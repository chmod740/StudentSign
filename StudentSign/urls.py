"""StudentSign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from web.views import login, logout, index, register, student, teacher, sign_in, sign_off, change_teacher_info, change_student_info

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login.html', login),
    url(r'^logout.html', logout),
    url(r'^index.html', index),
    url(r'^register.html', register),
    url(r'^student.html', student),
    url(r'^teacher.html', teacher),
    url(r'^sign_in.html', sign_in),
    url(r'^sign_off.html', sign_off),
    url(r'^$', index),
    url(r'^change_student_info.html', change_student_info),
    url(r'^change_teacher_info.html', change_teacher_info),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': '/home/ubuntu/py-web/StudentSign/static'})
]
